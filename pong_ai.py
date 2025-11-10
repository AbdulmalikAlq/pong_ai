import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game constants
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 20
PLAYER_SPEED = 7
AI_SPEED = 6
BALL_SPEED = 7

# Game objects
player = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai = pygame.Rect(25, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_dx = random.choice([-1, 1]) * BALL_SPEED
ball_dy = random.uniform(-1, 1) * BALL_SPEED

clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
player_score = 0
ai_score = 0

def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = random.choice([-1, 1]) * BALL_SPEED
    ball_dy = random.uniform(-1, 1) * BALL_SPEED

def draw():
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, player)
    pygame.draw.rect(WIN, WHITE, ai)
    pygame.draw.ellipse(WIN, WHITE, ball)
    pygame.draw.aaline(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{ai_score}   {player_score}", True, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()

def move_ai():
    # Simple prediction: AI moves toward predicted y position of the ball
    if ball_dx < 0:
        # Predict ball Y position when it reaches AI side
        future_y = ball.centery + ball_dy * ((ball.centerx - ai.centerx) / abs(ball_dx))
        # Bounce prediction off walls
        while future_y < 0 or future_y > HEIGHT:
            if future_y < 0:
                future_y = -future_y
            elif future_y > HEIGHT:
                future_y = 2 * HEIGHT - future_y

        # Move AI toward predicted Y
        if ai.centery < future_y:
            ai.centery += AI_SPEED
        elif ai.centery > future_y:
            ai.centery -= AI_SPEED
    else:
        # Return to center when ball moves away
        if ai.centery < HEIGHT // 2:
            ai.centery += AI_SPEED / 2
        elif ai.centery > HEIGHT // 2:
            ai.centery -= AI_SPEED / 2

    ai.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

def main():
    global ball_dx, ball_dy, player_score, ai_score

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += PLAYER_SPEED

        # Move AI
        move_ai()

        # Move Ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall collision
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Paddle collision (adds bounce angles)
        if ball.colliderect(player):
            offset = (ball.centery - player.centery) / (PADDLE_HEIGHT / 2)
            ball_dx *= -1
            ball_dy = offset * BALL_SPEED
        if ball.colliderect(ai):
            offset = (ball.centery - ai.centery) / (PADDLE_HEIGHT / 2)
            ball_dx *= -1
            ball_dy = offset * BALL_SPEED

        # Scoring
        if ball.left <= 0:
            player_score += 1
            reset_ball()
        elif ball.right >= WIDTH:
            ai_score += 1
            reset_ball()

        draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
