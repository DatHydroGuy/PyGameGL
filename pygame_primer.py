import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
from random import randint


# define a player class by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((75, 25))
        # self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load('jet.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()        # self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20, 10))
        # self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load('missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), randint(0, SCREEN_HEIGHT))
        )
        self.speed = randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), randint(0, SCREEN_HEIGHT))
        )
        self.speed = randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# define constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

# create the drawing surface (screen)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 250)
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

# instantiate player
player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

# main loop
running = True
while running:

    # process user inputs
    for event in pygame.event.get():
        # did the user press a key?
        if event.type == KEYDOWN:
            # was it the escape key? If so, then exit program
            if event.key == K_ESCAPE:
                running = False
        # did the user click the close window button? If so, then exit program
        elif event.type == QUIT:
            running = False
        elif event.type == ADD_ENEMY:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()
            all_sprites.add(new_cloud)
            clouds.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    # fill the background with white
    screen.fill((135, 206, 250))

    # draw all sprites on the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # update the display
    pygame.display.flip()

    clock.tick(30)

# exit pygame
pygame.quit()
