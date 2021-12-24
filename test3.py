from typing_extensions import runtime
import pygame
import os
from tools import scale_image, blit_rotate_center

""" Game Settings """

# Center the Screen
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Window Creation
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curfew")  # Title

BACKGROUND = pygame.image.load("assets/background_1.png")
BACKGROUND_BORDER = pygame.image.load("assets/background_1_mask.png")
BACKGROUND_BORDER_MASK = pygame.mask.from_surface(BACKGROUND_BORDER)
BORDER = pygame.Rect(0, 0, 10, WIDTH)

# Game Declarations
FPS = 60
MAX_VSPEED = 2
vspeed = MAX_VSPEED
V_ACCELERATION = 0.2
TURN = 0
turn_angle = 0

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SLATE_GRAY = (112, 128, 144)
BLUE = (0, 0, 245)

# Player sprite
PLAYER_WIDTH, PLAYER_HEIGHT = 32, 32
PLAYER_IMAGE = pygame.image.load(os.path.join("assets", "player_001.png"))
PLAYER = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_MASK = pygame.mask.from_surface(PLAYER)

# enemy sprite
ENEMY_1 = pygame.transform.rotate(
    pygame.image.load(os.path.join("assets", "camera_002.png")), TURN
)

# pygame.transform.rotate(x,y)S
# pygame.transform.scale(x,y)
# pygame.draw.rect(WIN, BLACK, 640, 360, 20, 20)


class Abstract_Enemy:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = turn_angle
        self.x, self.y = self.START_POS

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)


# class Player:
class player(pygame.sprite.Sprite):
    # IMG = PLAYER
    def __init__(self, pos_x, pos_y):
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/player_001.png"))
        self.sprites.append(pygame.image.load("assets/player_002.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.left = False
        self.x, self.y = pos_x, pos_y

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    # Collision
    def collide(self, mask, x=0, y=0):
        player_mask = pygame.mask.from_surface(self.IMG)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(player_mask, offset)
        return poi

    def draw(self, win):
        if self.left:
            self.image = pygame.transform.flip(self.image, False, True)
            win.blit(self.image, self.x, self.y)
        else:
            win.blit(self.image, self.x, self.y)


class enemy_camera(Abstract_Enemy):
    IMG = ENEMY_1
    START_POS = (190, 200)


# Draw objects
def draw_window(player_o, enemy_o):
    # Background
    WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0, 0))

    # Box
    # pygame.draw.rect(WIN, BLACK, BORDER)

    player_o.draw(WIN)
    enemy_o.draw(WIN)

    player_o.update()

    pygame.display.update()


def player_movement(keys_pressed, player_o):
    if (
        keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]
    ) and player_o.x - vspeed > 0:  # LEFT
        offset = (int(player_o.x - vspeed), int(player_o.y))
        overlap = BACKGROUND_BORDER_MASK.overlap(PLAYER_MASK, (offset))
        player_o.left = True
        if not overlap:
            player_o.x -= vspeed
    if (
        keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]
    ) and player_o.x - vspeed < WIDTH - PLAYER_WIDTH:  # RIGHT
        offset = (int(player_o.x + vspeed), int(player_o.y))
        overlap = BACKGROUND_BORDER_MASK.overlap(PLAYER_MASK, (offset))
        player_o.left = False
        if not overlap:
            player_o.x += vspeed
    if (
        keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]
    ) and player_o.y - vspeed > 0:  # UP
        offset = (int(player_o.x), int(player_o.y - vspeed))
        overlap = BACKGROUND_BORDER_MASK.overlap(PLAYER_MASK, (offset))
        if not overlap:
            player_o.y -= vspeed
    if (
        keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]
    ) and player_o.y + vspeed < HEIGHT - PLAYER_HEIGHT:  # DOWN
        offset = (int(player_o.x), int(player_o.y + vspeed))
        overlap = BACKGROUND_BORDER_MASK.overlap(PLAYER_MASK, (offset))
        if not overlap:
            player_o.y += vspeed


def main():
    player_o = player(50, 290)
    enemy_o = enemy_camera(4, 4)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        # player_o.x += 1

        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player_o)

        draw_window(player_o, enemy_o)

    pygame.quit()


if __name__ == "__main__":
    main()
