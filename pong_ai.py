import pygame
import sys
import random

pygame.init()

# Window setup
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 150, 255)

font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# Global settings
ball_size = 20
difficulty = "Medium"

# Game constants
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PLAYER_SPEED = 7

def draw_text(text, y, color=WHITE):
    txt = font.render(text, True, color)
    WIN.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))

def main_menu():
    global difficulty, ball_size

    selected = 0
    options = ["Play", "Settings", "Quit"]
    while True:
        WIN.fill(BLACK)
        draw_text("🏓 PING PONG AI", 100)
        for i, option in enumerate(options):
            color = BLUE if i == selected else WHITE
            draw_text(option, 250 + i * 80, color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Play":
                        game_loop()
                    elif options[selected] == "Settings":
                        settings_menu()
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()

        clock.tick(30)

def settings_menu():
    global difficulty, ball_size
    levels = ["Easy", "Medium", "Hard"]
    selected = 0
    while True:
        WIN.fill(BLACK)
        draw_text("⚙️ SETTINGS", 100)
        draw_text(f"Difficulty: {difficulty}", 250)
        draw_text(f"Ball Size: {ball_size}", 330)
        draw_text("Press ← or → to adjust", 420, GRAY)
        draw_text("Press ESC to go back", 500, GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RIGHT:
                    if difficulty == "Easy":
                        difficulty = "Medium"
                    elif difficulty == "Medium":
                        difficulty = "Hard"
                elif event.key == pygame.K_LEFT:
                    if difficulty == "Hard":
                        difficulty = "Medium"
                    elif difficulty == "Medium":
                        difficulty = "Easy"
                elif event.key == pygame.K_UP:
                    ball_size = min(40, ball_size + 2)
                elif event.key == pygame.K_DOWN:
                    ball_size = max(10, ball_size - 2)

        clock.tick(30)

def game_loop():
    global difficulty, ball_size

    # Difficulty affects AI speed
    ai_speed = {"Easy": 4, "Medium": 6, "Hard": 8}[difficulty]
    BALL_SPEED = 7

    # Objects
    player = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ai = pygame.Rect(25, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
    ball_dx = random.choice([-1, 1]) * BALL_SPEED
    ball_dy = random.uniform(-1, 1) * BALL_SPEED

    player_score = 0
    ai_score = 0
    running = True

    def reset_ball():
        nonlocal ball_dx, ball_dy
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_dx = random.choice([-1, 1]) * BALL_SPEED
        ball_dy = random.uniform(-1, 1) * BALL_SPEED

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # go back to menu

        # Player move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += PLAYER_SPEED

        # AI move (predictive)
        if ball_dx < 0:
            predicted_y = ball.centery + ball_dy * ((ball.centerx - ai.centerx) / abs(ball_dx))
            while predicted_y < 0 or predicted_y > HEIGHT:
                if predicted_y < 0:
                    predicted_y = -predicted_y
                elif predicted_y > HEIGHT:
                    predicted_y = 2 * HEIGHT - predicted_y

            if ai.centery < predicted_y:
                ai.centery += ai_speed
            elif ai.centery > predicted_y:
                ai.centery -= ai_speed
        else:
            if ai.centery < HEIGHT // 2:
                ai.centery += ai_speed / 2
            elif ai.centery > HEIGHT // 2:
                ai.centery -= ai_speed / 2

        # Ball move
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall bounce
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Paddle bounce with angles
        if ball.colliderect(player):
            offset = (ball.centery - player.centery) / (PADDLE_HEIGHT / 2)
            ball_dx *= -1
            ball_dy = offset * BALL_SPEED
        if ball.colliderect(ai):
            offset = (ball.centery - ai.centery) / (PADDLE_HEIGHT / 2)
            ball_dx *= -1
            ball_dy = offset * BALL_SPEED

        # Score
        if ball.left <= 0:
            player_score += 1
            reset_ball()
        elif ball.right >= WIDTH:
            ai_score += 1
            reset_ball()

        # Draw
        WIN.fill(BLACK)
        pygame.draw.rect(WIN, WHITE, player)
        pygame.draw.rect(WIN, WHITE, ai)
        pygame.draw.ellipse(WIN, WHITE, ball)
        pygame.draw.aaline(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        score_text = font.render(f"{ai_score}   {player_score}", True, WHITE)
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
