"""Brick Breaker - versi modifikasi (power-up, multi-ball, level, nyawa)."""
import random
import sys
import pygame
from constants import *
from entities import Paddle, Ball, Brick
from powerups import random_powerup, apply_split, apply_paddle_shot


def build_bricks(level):
    bricks = []
    total_w = BRICK_COLS * BRICK_W + (BRICK_COLS - 1) * BRICK_GAP
    start_x = (WIDTH - total_w) // 2
    for r in range(BRICK_ROWS):
        hp = 3 if r < 2 else (2 if r < 4 else 1)
        if level == 1 and hp == 3:
            hp = 2
        for c in range(BRICK_COLS):
            x = start_x + c * (BRICK_W + BRICK_GAP)
            y = BRICK_TOP + r * (BRICK_H + BRICK_GAP)
            bricks.append(Brick(x, y, hp))
    return bricks


def new_ball_on_paddle(paddle):
    return Ball(paddle.rect.centerx, paddle.rect.top - BALL_RADIUS - 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Brick Breaker - Modifikasi")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 48, bold=True)

    paddle = Paddle()
    level, score, lives = 1, 0, START_LIVES
    bricks = build_bricks(level)
    balls = [new_ball_on_paddle(paddle)]
    launched = False
    powerups = []
    game_over = False

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_SPACE and not launched and not game_over:
                    launched = True
                    balls[0].set_direction(random.choice([-20, 20]), BALL_SPEED + level - 1)
                if e.key == pygame.K_r and game_over:
                    paddle = Paddle()
                    level, score, lives = 1, 0, START_LIVES
                    bricks = build_bricks(level)
                    balls = [new_ball_on_paddle(paddle)]
                    launched, powerups, game_over = False, [], False

        if not game_over:
            paddle.update(pygame.key.get_pressed())

            if not launched:                       # bola menempel di paddle
                balls[0].x = paddle.rect.centerx
                balls[0].y = paddle.rect.top - BALL_RADIUS - 1
            else:
                for b in balls:
                    b.update()
                    b.hit_paddle(paddle)
                    for brick in bricks:
                        if b.hit_brick(brick):
                            if brick.hit():
                                bricks.remove(brick)
                                score += 10
                                if random.random() < POWERUP_DROP_CHANCE:
                                    powerups.append(random_powerup(*brick.rect.center))
                            else:
                                score += 2
                            break

                # Bola jatuh: hanya dibuang. Game over HANYA jika semua bola habis.
                balls = [b for b in balls if not b.is_lost()]
                if not balls:
                    lives -= 1
                    powerups.clear()
                    if lives <= 0:
                        game_over = True
                    else:
                        balls = [new_ball_on_paddle(paddle)]
                        launched = False

            # Power-up jatuh & ditangkap paddle
            for p in powerups[:]:
                p.update()
                if p.rect.colliderect(paddle.rect):
                    if launched:
                        if p.kind == POWER_SPLIT:
                            apply_split(balls)
                        else:
                            apply_paddle_shot(balls, paddle)
                    powerups.remove(p)
                elif p.off_screen():
                    powerups.remove(p)

            # Level selesai
            if not bricks:
                level += 1
                bricks = build_bricks(level)
                balls = [new_ball_on_paddle(paddle)]
                launched, powerups = False, []

        # ---- Gambar ----
        screen.fill(BLACK)
        for brick in bricks:
            brick.draw(screen)
        for p in powerups:
            p.draw(screen)
        paddle.draw(screen)
        for b in balls:
            b.draw(screen)

        hud = font.render(f"Skor: {score}   Level: {level}   Nyawa: {lives}   Bola: {len(balls)}", True, WHITE)
        screen.blit(hud, (12, 14))
        if not launched and not game_over:
            msg = font.render("Tekan SPASI untuk meluncurkan bola", True, YELLOW)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))
        if game_over:
            t = big.render("GAME OVER", True, RED)
            screen.blit(t, t.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            s = font.render(f"Skor akhir: {score}  |  Tekan R untuk main lagi", True, WHITE)
            screen.blit(s, s.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        pygame.display.flip()


if __name__ == "__main__":
    main()
