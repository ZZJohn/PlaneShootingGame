import pygame
import random
from pygame.locals import *
from PIL import Image

def img_show(s, rect):
    im = Image.open(s)
    im = im.crop((rect[0], rect[1], rect[2]+rect[0], rect[3]+rect[1]))
    im.show()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
ENEMY2_HIT = 10

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for pr in player_rect:
            self.image.append(plane_img.subsurface(pr).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT-self.rect.height:
            self.rect.top = SCREEN_HEIGHT-self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.down_imgs = enemy_down_imgs
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed

class Enemy2(Enemy):
    def move(self):
        flag = random.randint(1, 10)
        if flag<=5 and self.rect.left >=0:
            self.rect.left -= 2*self.speed
            self.rect.top += self.speed
        else:
            self.rect.left += 2*self.speed

# img_show('resources/image/shoot.png', (0, 225, 170, 250))
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shoot Game")
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png').convert()
plane_img = pygame.image.load('resources/image/shoot.png').convert_alpha()

def play():
    player_rect = []
    player_rect.append(pygame.Rect(0, 99, 102, 126))
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    player_rect.append(pygame.Rect(165, 234, 102, 126))
    player_rect.append(pygame.Rect(330, 624, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_img.subsurface(bullet_rect)

    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_img.subsurface(enemy1_rect)
    enemy1_down_imgs = []
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

    enemy2_rect = pygame.Rect(335, 750, 170, 250)
    enemy2_img = plane_img.subsurface(enemy2_rect)
    enemy2_down_imgs = []
    enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 485, 170, 250)))
    enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 225, 170, 250)))
    enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(840, 750, 170, 250)))
    enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(675, 750, 170, 250)))

    player = Player(plane_img, player_rect, player_pos)
    enemies1 = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()

    shoot_tick = 0
    enemy1_tick = 0
    player_down_tick = 16
    enemy1_count = 0
    enemy2 = None
    enemy2_hit = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        #add bullets
        if not player.is_hit:
            if shoot_tick%15 == 0:
                player.shoot(bullet_img)
            shoot_tick += 1
            if shoot_tick >= 15:
                shoot_tick = 0

        #add enemy1
        if enemy1_tick%50 == 0 and enemy1_count<=10:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH-enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy1_tick += 1
        if enemy1_tick == 50:
            enemy1_tick = 0

        if enemy1_count == 10 and enemy2==None:
            enemy2_pos = [(SCREEN_WIDTH-enemy2_rect.width)/2, 0]
            enemy2 = Enemy2(enemy2_img, enemy2_down_imgs, enemy2_pos)

        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom == 0:
                player.bullets.remove(bullet)
            if enemy2 != None:
                if pygame.sprite.collide_circle(enemy2, bullet):
                    enemy2_hit += 1
                    player.bullets.remove(bullet)

        for enemy1 in enemies1:
            enemy1.move()
            if pygame.sprite.collide_circle(enemy1, player):
                player.is_hit = True
                enemies1.remove(enemy1)
                enemies_down.add(enemy1)
                break
            if enemy1.rect.top>SCREEN_HEIGHT:
                enemies1.remove(enemy1)

        if enemy2!=None and enemy2_hit<=ENEMY2_HIT-1:
            enemy2.move()
            if pygame.sprite.collide_circle(enemy2, player):
                player.is_hit = True

        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy1 in enemies1_down:
            enemy1_count += 1
            enemies_down.add(enemy1)

        screen.fill(0)
        screen.blit(background, (0, 0))

        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            player.img_index = shoot_tick / 8
        else:
            player.img_index = player_down_tick / 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_tick += 1
            if player_down_tick > 47:
                running = False

        if enemy2!=None:
            if enemy2.rect.top <= SCREEN_HEIGHT:
                screen.blit(enemy2.image, enemy2.rect)
            else:
                enemy2 = None
                enemy1_count = 0
                enemy2_hit = 0
            if enemy2_hit >=ENEMY2_HIT:
                if enemy2.down_index > 15:
                    enemy2 = None
                    enemy1_count = 0
                    enemy2_hit = 0
                else:
                    screen.blit(enemy2.down_imgs[enemy2.down_index/4], enemy2.rect)
                    enemy2.down_index += 1

        for enemy_down in enemies_down:
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index / 2], enemy_down.rect)
            enemy_down.down_index += 1

        player.bullets.draw(screen)
        enemies1.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

    font = pygame.font.Font(None, 48)
    text2 = font.render("R to Restart, Q to Quit", True, (255, 0, 0))
    text2_rect = text2.get_rect()
    text2_rect.centerx = screen.get_rect().centerx
    text2_rect.centery = screen.get_rect().centery+48
    screen.blit(game_over, (0, 0))
    screen.blit(text2, text2_rect)
    pygame.display.update()

play()
while 1:
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_q]:
        pygame.quit()
        exit()
    if key_pressed[K_r]:
        play()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()