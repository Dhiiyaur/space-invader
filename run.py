import pygame as pg
from  pygame import mixer
import random
import math
import os

# loc
BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE + '\data')

pg.init()
# display
screen = pg.display.set_mode((500,500))

#Title and icon
pg.display.set_caption("Space Invader")
icon = pg.image.load('ufo.png')
pg.display.set_icon(icon)

#BG
BG = pg.image.load('BG.png').convert()
#BG_sound
mixer.music.load('bg_sound.wav')
mixer.music.play(-1)

#player
playerImg = pg.image.load('player.png')
playerX = 200
playerY = 450
playerX_change = 0
playerY_change = 0

#enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load('ghost.png'))
    enemyX.append(random.randint(0, 450))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Bullet
 # State_ ready --> you can't see bullet on thee screen
 #        Fire  --> bullet moving on the screen

bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 1.2
bullet_state = "ready"

#score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 25)

text_x = 10
text_y = 10

#game_over_text
game_over_font = pg.font.Font('freesansbold.ttf', 40)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render(('GAME OVER'), True, (255, 255, 255))
    screen.blit(over_text, (120, 200))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y+3))

#collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
    if distance < 20:
        return True
    else:
        return False

def collision_player(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2))
    if distance < 20:
        return True
    else:
        return False


#looping
running = True
while running:

    #BG_Color
    screen.fill((0, 0, 0))
    screen.blit(BG,(0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    #controller
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -0.6
            if event.key == pg.K_RIGHT:
                playerX_change = 0.6
            if event.key == pg.K_UP:
                playerY_change = -0.6
            if event.key == pg.K_DOWN:
                playerY_change = 0.6

            if event.key == pg.K_SPACE:
                if bullet_state is "ready":
                #sound bullet
                    bullet_sound = mixer.Sound('bullet.wav')
                    bullet_sound.play()
                # where ship location (x) and y location di the map
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

    #bulletX
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                playerY_change = 0

    #Boundaries player and enemy
    playerY += playerY_change
    playerX += playerX_change
    if  playerX <= 0:
            playerX_change = 0
    elif playerX >= 468:
            playerX_change = 0
    elif playerY <= 0:
            playerY_change = 0
    elif playerY >= 468:
            playerY_change = 0


    #number oof enemy move
    for i in range(num_of_enemies):

    #game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        collision2 = collision_player(enemyX[i], enemyY[i], playerX, playerY)
        if collision2:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            game_over_text()
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            break

        enemyX[i] += enemyX_change[i]
        if  enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 468:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #collision
        collision1 = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision1:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_state = "ready"
            bulletY = 0
            score_value += 1
            enemyX[i] = random.randint(0, 450)
            enemyY[i] = random.randint(50, 100)

        enemy(enemyX[i], enemyY[i], i)
    #bullet movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(text_x, text_y)
    pg.display.update()
