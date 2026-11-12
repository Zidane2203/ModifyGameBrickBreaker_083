"""Power-up: kapsul jatuh dari brick, efek aktif saat ditangkap paddle."""
import random
import pygame
from constants import *
from entities import Ball


class PowerUp:
    def __init__(self, x, y, kind):
        self.kind = kind
        self.rect = pygame.Rect(0, 0, POWERUP_SIZE, POWERUP_SIZE)
        self.rect.center = (x, y)
        self.color = CYAN if kind == POWER_SPLIT else PINK
        self.label = "S" if kind == POWER_SPLIT else "P"
        self.font = pygame.font.SysFont("consolas", 18, bold=True)

    def update(self):
        self.rect.y += POWERUP_FALL_SPEED

    def off_screen(self):
        return self.rect.top > HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=6)
        txt = self.font.render(self.label, True, BLACK)
        screen.blit(txt, txt.get_rect(center=self.rect.center))


def random_powerup(x, y):
    return PowerUp(x, y, random.choice([POWER_SPLIT, POWER_PADDLE]))


def apply_split(balls):
    """Power-up 1: setiap bola yang ada memecah jadi 2 (bola baru muncul dari bola itu)."""
    new_balls = []
    for b in balls:
        if len(balls) + len(new_balls) >= MAX_BALLS:
            break
        nb = Ball(b.x, b.y, color=CYAN)
        angle_now = _angle_of(b)
        nb.set_direction(angle_now + random.choice([-35, 35]), max(b.speed, BALL_SPEED))
        if nb.vy > 0:               # usahakan pecahan naik dulu
            nb.vy = -abs(nb.vy)
        new_balls.append(nb)
    balls.extend(new_balls)


def apply_paddle_shot(balls, paddle):
    """Power-up 2: 2 bola baru ditembakkan dari paddle (pin player)."""
    for angle in (-25, 25):
        if len(balls) >= MAX_BALLS:
            break
        nb = Ball(paddle.rect.centerx + angle, paddle.rect.top - BALL_RADIUS - 1, color=PINK)
        nb.set_direction(angle, BALL_SPEED)
        balls.append(nb)


def _angle_of(ball):
    import math
    return math.degrees(math.atan2(ball.vx, -ball.vy))
