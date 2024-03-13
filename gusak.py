import pygame
import random
import os

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
FONT = pygame.font.SysFont('Verdana', 20)


main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = 'Player_Animated'
PLAYER_IMAGES_NAMES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
#player.fill(COLOR_BLACK)
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_rect = player_rect.move(WIDTH/3, HEIGHT/2)

score = 0
player_image_index = 0

#Define enemy
def create_enemy():
    enemy_size = (205,72)
    enemy = pygame.Surface(enemy_size)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_size = (enemy.get_rect().width, enemy.get_rect().height)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    #if enemy_rect[1] < enemy_size[1] / 2:
    #    enemy_rect[1] = enemy_size[1] / 2
    if enemy_rect[1] > HEIGHT - enemy_size[1]:
        enemy_rect[1] = HEIGHT - enemy_size[1]
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, random.randint(1000, 3000))
enemies = []

#Define bonus
def create_bonus():
    bonus_size = (179, 298)
    bonus = pygame.Surface(bonus_size)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_size = (bonus.get_rect().width, bonus.get_rect().height)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), -bonus_size[1], *bonus_size)
    if bonus_rect[0] < bonus_size[0] / 2:
        bonus_rect[0] = bonus_size[0] / 2
    if bonus_rect[0] > WIDTH - bonus_size[0]:
        bonus_rect[0] = WIDTH - bonus_size[0]
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, random.randint(1000, 3000))
bonuces = []

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

playing = True
while playing == True:
    FPS.tick(120)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuces.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES_NAMES[player_image_index]))
            player_image_index +=1
            if player_image_index >= len(PLAYER_IMAGES_NAMES):
                player_image_index = 0


    #main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    bg_X2 -= bg_move
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()



    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuces:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuces.pop(bonuces.index(bonus))

    

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuces:
        if bonus[1].bottom > HEIGHT:
            bonuces.pop(bonuces.index(bonus))

   