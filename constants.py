"""Konstanta game Brick Breaker (versi modifikasi)."""

WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna
BLACK = (15, 15, 25)
WHITE = (240, 240, 240)
GRAY = (120, 120, 140)
RED = (231, 76, 60)
ORANGE = (230, 126, 34)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
PURPLE = (155, 89, 182)
CYAN = (26, 188, 156)
PINK = (255, 105, 180)

# Paddle
PADDLE_W, PADDLE_H = 110, 14
PADDLE_SPEED = 9

# Bola
BALL_RADIUS = 8
BALL_SPEED = 6
MAX_BALLS = 12          # batas bola agar tidak lag

# Brick
BRICK_COLS = 10
BRICK_ROWS = 6
BRICK_W = 70
BRICK_H = 24
BRICK_GAP = 6
BRICK_TOP = 60

# Power-up
POWERUP_DROP_CHANCE = 0.25   # peluang brick menjatuhkan power-up
POWERUP_FALL_SPEED = 3
POWERUP_SIZE = 26
POWER_SPLIT = "split"        # bola memecah dari bola itu sendiri
POWER_PADDLE = "paddle"      # bola memecah dari paddle (pin player)

# Nyawa
START_LIVES = 3
