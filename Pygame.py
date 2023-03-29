import pygame
from pygame import mixer
from sys import exit
from random import randint, choice

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        playerWalk1 = pygame.image.load('Graphic/Player/player_walk_1.png').convert_alpha()
        playerWalk2 = pygame.image.load('Graphic/Player/player_walk_2.png').convert_alpha()
        self.playerJump = pygame.image.load('Graphic/Player/jump.png').convert_alpha()
        self.playerIndex = 0
        self.playerWalk = [playerWalk1, playerWalk2]
        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jumpSound = pygame.mixer.Sound('Audio/jump.mp3')

    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jumpSound.play()
            self.gravity -= 20

    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0

    def anime(self):
        if self.rect.bottom < 300: self.image = self.playerJump
        else:
            self.playerIndex = self.playerIndex + 0.1 if self.playerIndex <= len(self.playerWalk) - 1 else - len(self.playerWalk)
            self.image = self.playerWalk[int(self.playerIndex)]

    def update(self):
        self.jump()
        self.applyGravity()
        self.anime()

snailTimer = pygame.USEREVENT + 1
pygame.time.set_timer(snailTimer, 500)

flyTimer = pygame.USEREVENT + 2
pygame.time.set_timer(flyTimer, 200)

class Obastacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            flySurface1 = pygame.image.load('Graphic/Fly/Fly1.png').convert_alpha()
            flySurface2 = pygame.image.load('Graphic/Fly/Fly2.png').convert_alpha()
            self.frame = [flySurface1, flySurface2]
            yPos = 200 if randint(0, 1) else 280
        else:
            snailSurface1 = pygame.image.load('Graphic/Snail/snail1.png').convert_alpha()
            snailSurface2= pygame.image.load('Graphic/Snail/snail2.png').convert_alpha()
            self.frame = [snailSurface1, snailSurface2]
            yPos = 300
        self.animationIndex = 0
        self.image = self.frame[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), yPos))

    def animationState(self):
        self.animationIndex += 0.07 if type == 'snail' else 0.05
        if self.animationIndex >= len(self.frame): self.animationIndex = 0
        self.image = self.frame[int(self.animationIndex)]
    def destroy(self):
        if self.rect.x <= -50: self.kill()

    def update(self):
        self.animationState()
        global acc
        if acc < 20 and pygame.time.get_ticks() - startTime > 20000: acc += 0.01
        self.rect.x -= acc
        self.destroy()

startTime, score = 0, 0
gameActive = False
acc = 3

def displayScore():
    currentTime = pygame.time.get_ticks() - startTime
    scoreSurf = textFont.render(f'{currentTime // 100}', False, (64, 64, 64))
    scoreRect = scoreSurf.get_rect(center = (400, 50))
    screen.blit(scoreSurf, scoreRect)

def collision(player, obstacles):
    global gameActive
    if obstacles:
        for rect in obstacles:
            if player.colliderect(rect):
                gameActive = False

def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    return True
def playerAni():
    global playerSurf, playerIndex
    if playerRect.bottom < 300: playerSurf = playerJump
    else:
        playerIndex = playerIndex + 0.1 if playerIndex <= len(playerWalk) - 1 else - len(playerWalk)
        playerSurf = playerWalk[int(playerIndex)]

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
textFont = pygame.font.Font('Font/Pixeltype.ttf', 50)

#group
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacleGroup = pygame.sprite.Group()

skySurface = pygame.image.load('Graphic/Sky.png').convert()
groundSurface = pygame.image.load('Graphic/ground.png').convert()

#obstacles
#snail

#fly


obstacleRectList = []

playerWalk1 = pygame.image.load('Graphic/Player/player_walk_1.png').convert_alpha()
playerWalk1 = pygame.transform.rotozoom(playerWalk1, 0, 0.9)

playerWalk2 = pygame.image.load('Graphic/Player/player_walk_2.png').convert_alpha()
playerWalk2 = pygame.transform.rotozoom(playerWalk2, 0, 0.9)

playerIndex = 0
playerWalk = [playerWalk1, playerWalk2]
playerJump = pygame.image.load('Graphic/Player/jump.png').convert_alpha()
playerJump = pygame.transform.rotozoom(playerJump, 0, 0.9)

playerSurf = playerWalk[playerIndex]
playerRect = playerSurf.get_rect(midbottom = (80, 300))

playerGravity, startTime = 0, 0

playerStand = pygame.image.load('Graphic/Player/player_stand.png').convert_alpha()
playerStand = pygame.transform.rotozoom(playerStand, 0, 2)
playerStandRect = playerStand.get_rect(center = (400, 200))

gameName = textFont.render('Kario', False, (111, 196, 169))
gameNameRect = gameName.get_rect(center = (400, 80))

gameMessage = textFont.render('Press Space to run', False, (111, 196, 169))
gameMessageRect = gameMessage.get_rect(center = (400, 330))

#timer
obstacleTimer = pygame.USEREVENT 
pygame.time.set_timer(obstacleTimer, 1500)

#music
background = pygame.mixer.Sound('Audio/music.wav')
background.set_volume(0.5)
background.play(loops = -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #jump
        if gameActive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playerRect.collidepoint(event.pos) and playerRect.bottom == 300: playerGravity = -20 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE and playerRect.bottom == 300: playerGravity = -20 

            if event.type == pygame.KEYUP: pass
            if event.type == obstacleTimer: 
                obstacleGroup.add(Obastacle(choice(['fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                acc = 5
                gameActive = True
                startTime = pygame.time.get_ticks() 
                obstacleRectList.clear()
                playerRect.midbottom = (80, 300)
                playerGravity = 0
       
    if gameActive:
        screen.blit(skySurface, (0, 0))
        screen.blit(groundSurface, (0, 300))
        score = displayScore()
        
        player.draw(screen)
        player.update()
        obstacleGroup.draw(screen)
        obstacleGroup.update()

        #collision
        gameActive = collisionSprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(playerStand, playerStandRect)

        scoreMessage = textFont.render(f'Your Score {score}', False,(111, 196, 169))
        scoreRect = scoreMessage.get_rect(center = (400, 330))
        screen.blit(gameName, gameNameRect)

        if not score: screen.blit(gameMessage, gameMessageRect)
        else: screen.blit(scoreMessage, scoreRect)
    pygame.display.update()
    clock.tick(60)

