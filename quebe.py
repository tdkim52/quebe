__author__ = 'TDK'

#
# Timothy Kim
#
# Quebe platform game
#
#

import pygame
import sys

from pygame.locals import *

FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREY = (119, 136, 153)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):  # constructor
        super(Platform, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREY)

        self.rect = self.image.get_rect()

class Warp(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Warp, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        width = 35
        #height = 60
        height = 35
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.level = None

        self.jumpSound = pygame.mixer.Sound('assets/sounds/SFX_Jump_22.wav')
        self.jumpSound.set_volume(0.5)

    def update(self):   # moves the player
        self.calcGrav()

        # move left/right with collision detection
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # move up/down with collision detection
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def calcGrav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .40    # rate of acceleration, greater = more

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # on a platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.jumpSound.play()
            self.change_y = -10  # larger neg = stronger jump

    def goLeft(self):
        self.change_x = -6

    def goRight(self):
        self.change_x = 6

    def stop(self): # key up
        self.change_x = 0
        self.change_y = 0

class Level(object):    # superclass for level creation
    def __init__(self, player):
        self.platformList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.doorList = pygame.sprite.Group()
        self.player = player

        self.background = None

        self.world_shiftX = 0
        self.world_shiftY = 0

        self.startX = None
        self.startY = None

    def update(self):
        self.platformList.update()
        self.enemyList.update()
        self.doorList.update()

    def draw(self, screen):
        #screen.fill(BLUE)
        screen.blit(self.background, [0, 0])
        self.platformList.draw(screen)
        self.enemyList.draw(screen)
        self.doorList.draw(screen)

    def shiftWorldX(self, shift_x):
        self.world_shiftX += shift_x

        for door in self.doorList:
            door.rect.x += shift_x

        for platform in self.platformList:
            platform.rect.x += shift_x

        for enemy in self.enemyList:
            enemy.rect.x += shift_x

    def shiftWorldY(self, shift_y):
        self.world_shiftY += shift_y

        for door in self.doorList:
            door.rect.y += shift_y

        for platform in self.platformList:
            platform.rect.y += shift_y

        for enemy in self.enemyList:
            enemy.rect.y += shift_y

class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        #self.background = pygame.image.load('assets/background_purple.jpg').convert()
        self.background = pygame.image.load('assets/background_blue.jpg').convert()
        self.background.set_colorkey(WHITE)

        self.level_limitX = -100
        self.level_limitY = -300

        self.startX = 125
        self.startY = 100

        # [length, height, x, y]
        level = [[600, 70, 100, 400],
                 ]
        nextLvl = [[40, 60, 650, 340],
                   ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for door in nextLvl:
            warper = Warp(door[0], door[1])
            warper.rect.x = door[2]
            warper.rect.y = door[3]
            warper.player = self.player
            self.doorList.add(warper)

class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/background_blue.jpg').convert()
        self.background.set_colorkey(WHITE)

        self.level_limitX = -100
        self.level_limitY = -300

        self.startX = 125
        self.startY = 300

        # [length, height, x, y]
        level = [[600, 70, 100, 400],
                 [40, 60, 380, 340],
                 ]
        nextLvl = [[40, 60, 650, 340],
                   ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for door in nextLvl:
            warper = Warp(door[0], door[1])
            warper.rect.x = door[2]
            warper.rect.y = door[3]
            warper.player = self.player
            self.doorList.add(warper)

class Level_03(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/background_blue.jpg').convert()
        self.background.set_colorkey(WHITE)

        self.level_limitX = -900
        self.level_limitY = -300

        self.startX = 125
        self.startY = 300

        # [length, height, x, y]
        level = [[210, 30, 100, 400],
                 [210, 30, 500, 400],
                 [210, 30, 1000, 520],
                 ]
        nextLvl = [[40, 60, 1150, 460],
                   ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for door in nextLvl:
            warper = Warp(door[0], door[1])
            warper.rect.x = door[2]
            warper.rect.y = door[3]
            warper.player = self.player
            self.doorList.add(warper)

class Level_04(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/background_blue.jpg').convert()
        self.background.set_colorkey(WHITE)

        self.level_limitX = -100
        self.level_limitY = -300

        self.startX = 125
        self.startY = 300

        # [length, height, x, y]
        level = [[80, 80, 100, 480],
                 [80, 80, 180, 400],
                 [80, 80, 260, 320],
                 [80, 80, 340, 240],
                 [80, 80, 420, 160],
                 [80, 80, 500, 80],
                 [100, 20, 340, 540]
                 ]
        nextLvl = [[40, 60, 340, 480],
                   ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platformList.add(block)

        for door in nextLvl:
            warper = Warp(door[0], door[1])
            warper.rect.x = door[2]
            warper.rect.y = door[3]
            warper.player = self.player
            self.doorList.add(warper)

def main():

    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    pygame.mixer.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quebe")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    level_list.append(Level_04(player))

    current_level_num = 0
    current_level = level_list[current_level_num]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = current_level.startX
    player.rect.y = current_level.startY    #SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    pygame.mixer.music.load('assets/music/jhElegiac.ogg')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    music = True

    #jumpSound = pygame.mixer.Sound('assets/sounds/SFX_Jump_22.wav')

    #background_img = pygame.image.load('assets/background_blue.jpg').convert()

    done = False
    paused = False

    fpsClock = pygame.time.Clock()

    def restart():
        player.stop()
        current_level.shiftWorldX(-current_level.world_shiftX)
        current_level.shiftWorldY(-current_level.world_shiftY)
        #player.level = current_level
        player.rect.x = current_level.startX
        player.rect.y = current_level.startY

    def menu():
        fontObjR = pygame.font.Font("assets/fonts/Raleway-Regular.ttf", 32)
        fontObjQ = pygame.font.Font("assets/fonts/Raleway-Light.ttf", 20)
        fontObjF1 = pygame.font.Font("assets/fonts/Raleway-Light.ttf", 20)

        textSurfP = fontObjR.render("Paused", True, WHITE)
        textRectP = textSurfP.get_rect()
        textRectP.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/15))

        textSurfQ = fontObjQ.render("Press 'q' to Quit", True, WHITE)
        textRectQ = textSurfQ.get_rect()
        textRectQ.left = ((SCREEN_WIDTH/15))

        textSurfF1 = fontObjF1.render("Press 'F1' for Help", True, WHITE)
        textRectF1 = textSurfF1.get_rect()
        textRectF1.right = ((SCREEN_WIDTH/15)*14)

        textSurfM = fontObjQ.render("Press 'm' to Toggle Music", True, WHITE)
        textRectM = textSurfM.get_rect()
        textRectM.bottomleft = ((SCREEN_WIDTH/15), ((SCREEN_HEIGHT/15)*14))

        screen.blit(textSurfP, textRectP)
        screen.blit(textSurfQ, textRectQ)
        screen.blit(textSurfF1, textRectF1)
        screen.blit(textSurfM, textRectM)

        print(pygame.mixer.music.get_volume())
        pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if paused == False:
                        paused = True
                        menu()
                    elif paused == True:
                        paused = False
                    #pygame.quit()
                    #sys.exit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.goLeft()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.goRight()
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    #jumpSound.play()
                    player.jump()
                # restart level
                if event.key == pygame.K_r:
                    restart()
                if paused == True:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F1:
                        print("in-game help screen")
                if event.key == pygame.K_m:
                    if music == True:
                        pygame.mixer.music.pause()
                        music = False
                    else:
                        pygame.mixer.music.unpause()
                        music = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
                # skip to next level
                if event.key == pygame.K_TAB:
                    if current_level_num < len(level_list)-1:
                        player.stop()
                        current_level_num += 1
                        current_level = level_list[current_level_num]
                        player.level = current_level
                        player.rect.x = current_level.startX
                        player.rect.y = current_level.startY

        if paused == False:
            active_sprite_list.update()
            current_level.update()

            # checks if warp door has been reached
            door_hit_list = pygame.sprite.spritecollide(player, player.level.doorList, False)
            for door in door_hit_list:
                if current_level_num < len(level_list)-1:
                    player.stop()
                    current_level_num += 1
                    current_level = level_list[current_level_num]
                    player.level = current_level
                    player.rect.x = current_level.startX
                    player.rect.y = current_level.startY

            # player near right, shift world left
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shiftWorldX(-diff)

            # player near left, shift world right
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_level.shiftWorldX(diff)

            # player near top, shift world down
            if player.rect.top <= 120:
                diff = 120 - player.rect.top
                player.rect.top = 120
                current_level.shiftWorldY(diff)

            #player near bot, shift world up
            if player.rect.bottom >= 500:
                diff = player.rect.bottom - 500
                player.rect.bottom = 500
                current_level.shiftWorldY(-diff)

            # end of current level boundaries
            current_positionX = player.rect.x + current_level.world_shiftX
            current_positionY = player.rect.y + current_level.world_shiftY
            if current_positionX < current_level.level_limitX:
                restart()
            if current_positionY < current_level.level_limitY:
                restart()

            # all drawing BELOW
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            # all drawing ABOVE

            fpsClock.tick(FPS)

            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()