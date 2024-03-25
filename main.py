from typing_extensions import runtime
import time
import pygame
import os
from tools import scale_image, blit_rotate_center, blit_text_center

pygame.font.init()

""" Game Settings """
# Center the Screen
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Window Creation
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curfew")  # Title

BACKGROUND = pygame.image.load(os.path.join('curfew/assets', 'background_1.png'))
BACKGROUND_BORDER = pygame.image.load(os.path.join('curfew/assets', 'background_1_mask.png'))
BACKGROUND_BORDER_MASK = pygame.mask.from_surface(BACKGROUND_BORDER)
BORDER = pygame.Rect(0, 0, 10, WIDTH)
FINISH = pygame.image.load(os.path.join('curfew/assets', 'finish.png'))
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (785, 315)

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
PLAYER_IMAGE = pygame.image.load(os.path.join('curfew/assets', 'player_001.png'))
PLAYER = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_MASK = pygame.mask.from_surface(PLAYER)

# enemy sprite
ENEMY_1 = pygame.transform.rotate(
    pygame.image.load(os.path.join('curfew/assets', 'camera_002.png')), TURN
)

MAIN_FONT = pygame.font.SysFont("79", 44)

# pygame.transform.rotate(x,y)S
# pygame.transform.scale(x,y)
# pygame.draw.rect(WIN, BLACK, 640, 360, 20, 20)


# Levels
class GameInfo:
    LEVELS = 3

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


# class enemies
class Abstract_Enemy:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = turn_angle
        self.x, self.y = self.ENEMY_START_POS

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)


class enemy_camera(Abstract_Enemy):
    IMG = ENEMY_1
    ENEMY_START_POS = (190, 200)


# class Player
class player:
    def __init__(self):
        self.img = PLAYER
        self.player_start_pos = (50, 290)
        self.x, self.y = self.player_start_pos
        self.angle = turn_angle

    # Collision
    def collide(self, mask, x=0, y=0):
        player_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(player_mask, offset)
        return poi

    def reset(self):
        # self.x, self.x = self.player_start_pos
        self.x, self.y = (50, 290)

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)


# Draw objects
def draw_window(win, images, player_o, enemy_o, game_info):

    for img, pos in images:
        win.blit(img, pos)

    # Level Info
    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, WHITE)
    win.blit(
        level_text,
        (WIDTH - level_text.get_width() - 10, HEIGHT - level_text.get_height() - 10),
    )

    # Time Info
    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}", 1, WHITE)
    win.blit(
        time_text,
        (WIDTH - time_text.get_width() - 10, HEIGHT - time_text.get_height() - 40),
    )

    player_o.draw(win)
    enemy_o.draw(win)

    pygame.display.update()


def player_movement(keys_pressed, player_o):
    if (
        keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]
    ) and player_o.x - vspeed > 0:  # LEFT
        offset = (int(player_o.x - vspeed), int(player_o.y))
        overlap = BACKGROUND_BORDER_MASK.overlap(PLAYER_MASK, (offset))
        if not overlap:
            player_o.x -= vspeed
    if (
        keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]
    ) and player_o.x - vspeed < WIDTH - PLAYER_WIDTH:  # RIGHT
        offset = (int(player_o.x + vspeed), int(player_o.y))
        overlap = BACKGROUND_BORDER_MASK.overlap(PLAYER_MASK, (offset))
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
    images = [(BACKGROUND, (0, 0)), (FINISH, FINISH_POS)]
    player_o = player()
    enemy_o = enemy_camera(4, 4)
    clock = pygame.time.Clock()
    game_info = GameInfo()
    run = True

    while run:
        clock.tick(FPS)

        draw_window(WIN, images, player_o, enemy_o, game_info)

        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player_o)

        if player_o.collide(FINISH_MASK, *FINISH_POS) != None:
            player_o.reset()

    pygame.quit()


if __name__ == "__main__":
    main()
