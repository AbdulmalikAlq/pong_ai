import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong AI")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 150, 255)
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# Default settings
ball_size = 20
difficulty = "Medium"
WIN_SCORE = 10

# Paddle constants
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PLAYER_SPEED = 7

def draw_text(text, y, color=WHITE):
    txt = font.render(text, True, color)
    WIN.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y))

def main_menu():
    options = ["Play", "Settings", "Quit"]
    selected = 0
    while True:
        WIN.fill(BLACK)
        draw_text("🏓 PING PONG AI", 100)
        for i, opt in enumerate(options):
            color = BLUE if i == selected else WHITE
            draw_text(opt, 250 + i * 80, color)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    if options[selected] == "Play": game_loop()
                    elif options[selected] == "Settings": settings_menu()
                    elif options[selected] == "Quit": pygame.quit(); sys.exit()
        clock.tick(30)

def settings_menu():
    global difficulty, ball_size
    while True:
        WIN.fill(BLACK)
        draw_text("⚙️ SETTINGS", 100)
        draw_text(f"Difficulty: {difficulty}", 250)
        draw_text(f"Ball Size: {ball_size}", 330)
        draw_text("←/→ change level | ↑/↓ change size", 430, GRAY)
        draw_text("ESC to go back", 500, GRAY)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_RIGHT:
                    difficulty = "Medium" if difficulty == "Easy" else "Hard" if difficulty == "Medium" else "Hard"
                if e.key == pygame.K_LEFT:
                    difficulty = "Medium" if difficulty == "Hard" else "Easy"
                if e.key == pygame.K_UP: ball_size = min(40, ball_size + 2)
                if e.key == pygame.K_DOWN: ball_size = max(10, ball_size - 2)
        clock.tick(30)

def game_loop():
    global difficulty, ball_size

    # Difficulty behavior
    ai_params = {
        "Easy": {"speed": 4, "error": 50, "reaction": 10},
        "Medium": {"speed": 6, "error": 20, "reaction": 5},
        "Hard": {"speed": 8, "error": 5, "reaction": 0}
    }[difficulty]

    BALL_SPEED = 7
    MAX_BALL_SPEED = 15
    player = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ai = pygame.Rect(25, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - ball_size//2, HEIGHT//2 - ball_size//2, ball_size, ball_size)

    ball_dx = random.choice([-1, 1]) * BALL_SPEED
    ball_dy = random.uniform(-1, 1) * BALL_SPEED

    player_score = 0
    ai_score = 0
    ai_reaction_timer = 0
    paused = False

    def reset_ball():
        nonlocal ball_dx, ball_dy
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_dx = random.choice([-1, 1]) * BALL_SPEED
        ball_dy = random.uniform(-1, 1) * BALL_SPEED

    def reset_round():
        nonlocal player_score, ai_score, BALL_SPEED
        player_score = 0
        ai_score = 0
        BALL_SPEED = 7
        reset_ball()

    def show_win_screen(winner):
        # simple blocking win screen: press Enter to return to menu
        while True:
            WIN.fill(BLACK)
            draw_text(f"{winner} Wins!", 180, BLUE)
            draw_text("Press ENTER to return to menu", 320, GRAY)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return
                    if e.key == pygame.K_ESCAPE:
                        return

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        # Player move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0: player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT: player.y += PLAYER_SPEED

        # Controls: P = pause, R = reset scores, ESC = quit round
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    paused = not paused
                if e.key == pygame.K_r:
                    reset_round()
        if paused:
            # draw paused overlay
            pause_txt = font.render("PAUSED - Press P to resume", True, GRAY)
            WIN.blit(pause_txt, (WIDTH//2 - pause_txt.get_width()//2, HEIGHT//2 - pause_txt.get_height()//2))
            pygame.display.flip()
            continue

        # AI move (with delay + error)
        ai_reaction_timer += 1
        if ai_reaction_timer > ai_params["reaction"]:
            ai_reaction_timer = 0
            # AI only reacts after its delay
            target_y = ball.centery + random.randint(-ai_params["error"], ai_params["error"])
            if ai.centery < target_y: ai.centery += ai_params["speed"]
            elif ai.centery > target_y: ai.centery -= ai_params["speed"]

        # Ball movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall bounce
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Paddle collision: reflect and slightly increase speed up to cap
        if ball.colliderect(player) or ball.colliderect(ai):
            offset = (ball.centery - (player.centery if ball.colliderect(player) else ai.centery)) / (PADDLE_HEIGHT / 2)
            # reverse X
            ball_dx *= -1
            # set Y based on where it hit
            ball_dy = offset * abs(ball_dx)
            # gradually increase speed but cap it
            ball_dx *= 1.05
            ball_dy *= 1.05
            # cap speeds
            if abs(ball_dx) > MAX_BALL_SPEED:
                ball_dx = MAX_BALL_SPEED * (1 if ball_dx > 0 else -1)
            if abs(ball_dy) > MAX_BALL_SPEED:
                ball_dy = MAX_BALL_SPEED * (1 if ball_dy > 0 else -1)

        # Score
        if ball.left <= 0:
            player_score += 1
            reset_ball()
        elif ball.right >= WIDTH:
            ai_score += 1
            reset_ball()

        # Win condition
        if player_score >= WIN_SCORE:
            show_win_screen("Player")
            return
        if ai_score >= WIN_SCORE:
            show_win_screen("AI")
            return

        # Draw
        WIN.fill(BLACK)
        pygame.draw.rect(WIN, WHITE, player)
        pygame.draw.rect(WIN, WHITE, ai)
        pygame.draw.ellipse(WIN, WHITE, ball)
        pygame.draw.aaline(WIN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        # Scores and labels
        score_text = font.render(f"{ai_score}   {player_score}", True, WHITE)
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        # Player/AI labels
        small = pygame.font.Font(None, 28)
        WIN.blit(small.render("AI", True, GRAY), (ai.x, ai.y - 24))
        WIN.blit(small.render("You", True, GRAY), (player.x - 10, player.y - 24))
        # Instructions
        instr = pygame.font.Font(None, 24).render("P: Pause | R: Reset scores | ESC: Exit to menu", True, GRAY)
        WIN.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT - 30))
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
