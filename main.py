import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))


# window settings
pygame.display.set_caption("SPACE INVADERS")
pygame.display.set_icon(pygame.image.load('icon.png'))

# player
playericon = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerchangeX = 0
playerchangeY = 0


def player(playerX, playerY):
    screen.blit(playericon, (playerX, playerY))


# enemy
num_of_enemies = 7

enemyicon = []
enemyX = []
enemyY = []
enemychangeX = []
enemychangeY = []

for i in range(num_of_enemies):
    enemyicon.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(5, 730))
    enemyY.append(random.randint(50, 80))
    enemychangeX.append(2)
    enemychangeY.append(60)


    def enemy(enemyX, enemyY, i):
        screen.blit(enemyicon[i], (enemyX[i], enemyY[i]))

# bullets
bulleticon = pygame.image.load('bullet.png')
bulletx = 0
bullety = 500
bulletchangex = 0
bulletchangey = 0
bulletstate = 1


def bullet(bulletx, bullety):
    if bulletstate == 0:
        screen.blit(bulleticon, (bulletx, bullety))


# collision
def iscollision(X1, Y1, X2, Y2):
    if math.sqrt((math.pow((X1 - X2), 2)) + (math.pow((Y1 - Y2), 2))) < 38:
        return True
    else:
        return False


# score
Score = 0


def showscore():
    font = pygame.font.Font('freesansbold.ttf', 32)
    score = font.render("score :" + str(Score), True, (225, 225, 225))
    screen.blit(score, (10, 10))


def gameover():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render("GAME OVER", True, (225, 225, 225))
    screen.blit(text, (210, 230))


# background
background = pygame.image.load('background.png')
backgroundaud = mixer.music.load('background.mp3')
mixer.music.play(-1)

# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerchangeX = -5
            if event.key == pygame.K_RIGHT:
                playerchangeX = 5
            if event.key == pygame.K_SPACE:  # bullet mechanics
                if bulletstate == 1:
                    mixer.Sound('bullet sound.mp3').play()
                    temp = playerX + 15
                    bulletx = temp
                    bulletchangey = 7
                    bulletstate = 0

        if event.type == pygame.KEYUP:
            playerchangeX = 0

    playerX += playerchangeX

    if bulletstate == 0:
        bullety -= bulletchangey
        if bullety < 0:
            bulletstate = 1
            bullety = 500

    for i in range(num_of_enemies):
        # game over
        if enemyY[i] >= 470:
            for j in range(num_of_enemies):
                enemyX[j]=3000
                enemyY[j] ==2000
            gameover()
            break

        # enemy movement
        enemyX[i] += enemychangeX[i]
        if enemyX[i] > 730:
            enemychangeX[i] = -3
            enemyY[i] += enemychangeY[i]
        if enemyX[i] < 5:
            enemychangeX[i] = 3
            enemyY[i] += enemychangeY[i]

        collision = iscollision(bulletx, bullety, enemyX[i], enemyY[i])
        if collision == True:
            bulletstate = 1
            bullety = 500
            Score += 1
            enemyX[i] = random.randint(5, 730)
            enemyY[i] = random.randint(50, 80)
        enemy(enemyX, enemyY, i)
    # boundary
    if playerX > 730:
        playerchangeX = 0
    elif playerX < 5:
        playerchangeX = 0
    showscore()
    bullet(bulletx, bullety)
    player(playerX, playerY)
    pygame.display.update()
