import pygame, random

pygame.init()

map_width = 800
map_height = 800
size = [map_width, map_height]
screen = pygame.display.set_mode(size)

# pygame already defines a lot of colors, we we just use them
colors = pygame.color.THECOLORS
pygame.display.set_caption("Natural Selection Game")
done = False
clock = pygame.time.Clock()

# just a simple generator to generate an id for each object
def id_generator():
    i = 0
    while True:
        i += 1
        yield i


ids = id_generator()

# just a helper function that wraps pygame.sprite.collide_mask
# to prevent a sprite from colliding with itself
def collide(a, b):
    if a.id == b.id:
        return False
    return pygame.sprite.collide_mask(a, b)


class Organism(pygame.sprite.Sprite):
    def __init__(self, id, org_list, color=None):
        pygame.sprite.Sprite.__init__(self, org_list)
        self.org_list = org_list
        self.id = id
        # Speed and direction
        self.change_x = random.randrange(0, 6)
        self.change_y = random.randrange(0, 6)

        # Dimensions
        width = random.randrange(5, 50)
        height = random.randrange(5, 50)
        x = random.randrange(0 + width, map_width - width)
        y = random.randrange(0 + height, map_height - height)
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.image = pygame.surface.Surface((width, height))
        self.image.fill(colors["hotpink2"])
        self.image.set_colorkey(colors["hotpink2"])

        # we either pass in the color, or create a random one
        self.color = color or random.choice(
            [colors["red"], colors["green"], colors["blue"]]
        )
        pygame.draw.ellipse(self.image, self.color, [0, 0, width, height])
        self.mask = pygame.mask.from_surface(self.image)

        # we keep track of collisions currently happening
        # so we only spawn one children for each collisions
        self.collisions = set()

        # just something to limit the number of organisms
        self.age = 0
        self.children = 0

    # Initiate movement
    def update(self):
        self.age += 1

        # we move by simply moving the rect
        # the Group's draw function will look that the rect attribute
        # to determine the position for drawing the image
        self.rect.move_ip(self.change_x, self.change_y)

        # we can make use of a lot of Rect's attributes to make
        # this computation simpler
        if self.rect.left < 0 or self.rect.right > map_width:
            self.change_x *= -1

        if self.rect.top < 0 or self.rect.bottom > map_height:
            self.change_y *= -1

        # only reproduce if we are at least 200 ticks old
        # so newly created organisms spwan new ones at the
        # very moment they spawned themself
        if self.age < 200:
            return

        # just a narbitary limit so the screen does not get too full
        if self.age > 500:
            print(str(self.id) + " died of age")

            # kill() removes the Sprite from all its Groups (which is only org_list at the moment)
            self.kill()
            return

        # just an arbitary limit so the screen does not get too full
        if self.children > 4:
            print(str(self.id) + " died of too many children")
            self.kill()
            return

        # check if we collided with another Sprite
        collided = pygame.sprite.spritecollideany(self, self.org_list, collide)

        # also check if this
        # - is a new collision
        # - the other organism is at least 200 ticks old
        # - there are not too many organisms at the screen at the moment
        if (
            collided
            and not collided.id in self.collisions
            and collided.age > 200
            and len(self.org_list) < 100
        ):

            # keep track of the current collision, so this code is not triggerd
            # every frame while the colliding organisms move other each other
            self.collisions.add(collided.id)
            collided.collisions.add(self.id)
            print(str(self.id) + " collided with " + str(collided.id))

            # we create a new color out of the colors of the parents
            r, g, b = (
                (self.color[0] + collided.color[0]) / 2,
                (self.color[1] + collided.color[1]) / 2,
                (self.color[2] + collided.color[2]) / 2,
            )
            color = [r, g, b]

            # let the color mutate sometimes for fun
            if random.randrange(0, 100) < 10:
                color[random.randrange(0, 3)] = random.randrange(0, 256)
                print(
                    "Offspring of "
                    + str(self.id)
                    + " and "
                    + str(collided.id)
                    + " mutates"
                )

            # create the new child with the new color
            Organism(next(ids), self.org_list, map(int, color))
            self.children += 1
            collided.children += 1
        else:
            # if there are currently no collisions, we clear the collisions set
            # so new collisions can happen
            self.collisions = set()


# we use a Group for all the draw/update/collision magic
org_list = pygame.sprite.Group()

for _ in range(15):
    Organism(next(ids), org_list)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # we just call update on the group so update is called
    # an every sprite in the group
    org_list.update()

    screen.fill(colors["white"])

    # same for drawing: just call draw on the group
    org_list.draw(screen)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
