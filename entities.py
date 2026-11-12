"""Objek utama game: Paddle, Ball, Brick."""
import math
import pygame
from constants import *


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, PADDLE_W, PADDLE_H)
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 30)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PADDLE_SPEED
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=7)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=7)


class Ball:
    def __init__(self, x, y, vx=0.0, vy=0.0, color=WHITE):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = vx, vy
        self.r = BALL_RADIUS
        self.color = color

    @property
    def speed(self):
        return math.hypot(self.vx, self.vy)

    def set_direction(self, angle_deg, speed):
        """Sudut 0 = lurus ke atas, positif = ke kanan."""
        a = math.radians(angle_deg)
        self.vx = speed * math.sin(a)
        self.vy = -speed * math.cos(a)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.r <= 0:
            self.x, self.vx = self.r, abs(self.vx)
        elif self.x + self.r >= WIDTH:
            self.x, self.vx = WIDTH - self.r, -abs(self.vx)
        if self.y - self.r <= 0:
            self.y, self.vy = self.r, abs(self.vy)

    def is_lost(self):
        return self.y - self.r > HEIGHT

    def hit_paddle(self, paddle):
        if self.vy > 0 and self._touches(paddle.rect):
            offset = (self.x - paddle.rect.centerx) / (paddle.rect.w / 2)
            offset = max(-1, min(1, offset))
            self.set_direction(offset * 60, max(self.speed, BALL_SPEED))
            self.y = paddle.rect.top - self.r
            return True
        return False

    def _touches(self, rect):
        cx = max(rect.left, min(self.x, rect.right))
        cy = max(rect.top, min(self.y, rect.bottom))
        return (self.x - cx) ** 2 + (self.y - cy) ** 2 <= self.r ** 2

    def hit_brick(self, brick):
        if not self._touches(brick.rect):
            return False
        dx = self.x - brick.rect.centerx
        dy = self.y - brick.rect.centery
        ox = brick.rect.w / 2 + self.r - abs(dx)
        oy = brick.rect.h / 2 + self.r - abs(dy)
        if ox < oy:
            self.vx = -self.vx
        else:
            self.vy = -self.vy
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)


class Brick:
    COLORS = {1: GREEN, 2: YELLOW, 3: RED}

    def __init__(self, x, y, hp):
        self.rect = pygame.Rect(x, y, BRICK_W, BRICK_H)
        self.hp = hp

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLORS.get(self.hp, PURPLE), self.rect, border_radius=4)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=4)
