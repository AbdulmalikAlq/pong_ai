import pygame
import sys

# Initialize pygame
pygame.init()

# Game window
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Player vs AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game constants
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PLAYER_SPEED = 7
AI_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 6, 6

# Player and AI positions
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai = pygame.Rect(5, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player_score = 0
ai_score = 0

def draw():
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, player)
    pygame.draw.rect(WIN, WHITE, ai)
    pygame.draw.ellipse(WIN, WHITE, ball)
    pygame.draw.aaline(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    score_text = font.render(f"{ai_score}   {player_score}", True, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.flip()

def ball_reset():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    BALL_SPEED_X *= -1  # change direction

def main():
    global BALL_SPEED_X, BALL_SPEED_Y, player_score, ai_score

    run = True
    while run:
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += PLAYER_SPEED

        # AI movement (follows the ball)
        if ai.centery < ball.centery:
            ai.y += AI_SPEED
        elif ai.centery > ball.centery:
            ai.y -= AI_SPEED
        ai.y = max(0, min(ai.y, HEIGHT - PADDLE_HEIGHT))

        # Ball movement
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        # Collision with top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y *= -1

        # Collision with paddles
        if ball.colliderect(player) or ball.colliderect(ai):
            BALL_SPEED_X *= -1

        # Scoring
        if ball.left <= 0:
            player_score += 1
            ball_reset()
        elif ball.right >= WIDTH:
            ai_score += 1
            ball_reset()

        draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
