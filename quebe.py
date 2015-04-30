__author__ = 'TDK'

#
# Timothy Kim
# W01011895
# April 29, 2015
#
# Quebe platform game
#
# references taken from texts:
# inventwithpython.com/makinggames.pdf
# programarcadegames.com
# pygame.org/docs
#
# Further documentation included in
# Quebe - Game Manual.pdf
#
#
# Release v0.1 - April 29, 2015
#

# requires pygame module to be installed
import pygame
import sys

from pygame.locals import *

# global constants
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREY = (119, 136, 153)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 115, 115)

# normal grey platforms/walls
class Platform(pygame.sprite.Sprite):
    # constructor
    def __init__(self, width, height):
        super(Platform, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREY)
        self.rect = self.image.get_rect()

# White Door warp
class Warp(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Warp, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

# pink enemy triangles, equilateral
class EnemyTri(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(EnemyTri, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.set_colorkey(BLACK)
        self.rect = pygame.draw.polygon(self.image, PINK, [[(width/2), 0], [0, height], [width, height]], 0)

# pink platforms/walls, death on contact
class EnemyPlat(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(EnemyPlat, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(PINK)
        self.rect = self.image.get_rect()

# user controlled Player black square
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # create square
        width = 35
        height = 35
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        # current speed
        self.change_x = 0
        self.change_y = 0

        # current level
        self.level = None

        # jump sound effect
        self.jumpSound = pygame.mixer.Sound('assets/sounds/SFX_Jump_22.wav')
        self.jumpSound.set_volume(0.5)

    # handles movement of player
    def update(self):
        self.calcGrav()

        # move left/right with collision detection of platforms
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # move up/down with collision detection of platforms
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platformList, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    # changes current speed location on y axis
    def calcGrav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .40    # rate of acceleration, greater = more
        # not on screen floor
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    # called on keypress, jumps
    def jump(self):
        # checks if on platform to jump by collision detection
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platformList, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.jumpSound.play()
            self.change_y = -10  # larger neg = stronger jump

    # called on keypress, moves player left
    def goLeft(self):
        self.change_x = -6
    # right
    def goRight(self):
        self.change_x = 6

    # called when jump cheat enabled
    def goUp(self):
        self.change_y = -6
    def goDown(self):
        self.change_y = 6

    # on key up sets speed to zero
    def stop(self):
        self.change_x = 0
        self.change_y = 0

# level superclass used for level creation
class Level(object):    # superclass for level creation
    def __init__(self, player):
        # lists of level objects
        self.platformList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.doorList = pygame.sprite.Group()

        self.player = player
        self.background = None

        # used for screen scrolling
        self.world_shiftX = 0
        self.world_shiftY = 0

        self.startX = None
        self.startY = None

    # moves all sprites
    def update(self):
        self.platformList.update()
        self.enemyList.update()
        self.doorList.update()

    # draws all objects to screen, background shifted for depth of field
    def draw(self, screen):
        screen.blit(self.background, (self.world_shiftX // 3, self.world_shiftY // 3))
        self.platformList.draw(screen)
        self.enemyList.draw(screen)
        self.doorList.draw(screen)

    # simulates scrolling horizontally
    def shiftWorldX(self, shift_x):
        self.world_shiftX += shift_x
        for door in self.doorList:
            door.rect.x += shift_x
        for platform in self.platformList:
            platform.rect.x += shift_x
        for enemy in self.enemyList:
            enemy.rect.x += shift_x

    # vertically
    def shiftWorldY(self, shift_y):
        self.world_shiftY += shift_y

        for door in self.doorList:
            door.rect.y += shift_y

        for platform in self.platformList:
            platform.rect.y += shift_y

        for enemy in self.enemyList:
            enemy.rect.y += shift_y

# each class is a unique level, calls on Level parent class
# level setup similar for 01-08
class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        # load background image
        self.background = pygame.image.load('assets/backgrounds/bluelvl1.png').convert()
        self.background.set_colorkey(BLACK)

        # set invisible map boundaries for death
        self.level_limitX = -100
        self.level_limitY = -300

        # starting position
        self.startX = 125
        self.startY = 125

        # [length, height, x, y]
        # grey platform placement
        level = [[600, 70, 100, 400],
                 ]
        # White Door placement
        nextLvl = [[40, 60, 650, 340],
                   ]

        # create objects, add to list, pass to Player
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

        self.background = pygame.image.load('assets/backgrounds/bluelvl2.png').convert()
        self.background.set_colorkey(BLACK)

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

        self.background = pygame.image.load('assets/backgrounds/blue.jpg').convert()
        self.background.set_colorkey(BLACK)

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

        self.background = pygame.image.load('assets/backgrounds/blue.jpg').convert()
        self.background.set_colorkey(BLACK)

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

class Level_05(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/backgrounds/blue.jpg').convert()
        self.background.set_colorkey(BLACK)

        self.level_limitX = -1000
        self.level_limitY = -300

        self.startX = 125
        self.startY = 125

        # [length, height, x, y]
        level = [[1100, 30, 50, 50],
                 [250, 30, 50, 200],
                 [30, 150, 50, 50],
                 [30, 340, 250, 200],
                 [100, 10, 420, 200],
                 [120, 80, 500, 80],
                 [100, 10, 575, 200],

                 [10, 20, 900, 300],
                 [250, 160, 1100, 50],
                 [300, 10, 1100, 250],

                 [40, 10, 250, 430],
                 [40, 10, 250, 320],
                 [125, 10, 250, 540]
                 ]
        nextLvl = [[40, 60, 1360, 190],
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

class Level_06(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/backgrounds/blue.jpg').convert()
        self.background.set_colorkey(BLACK)

        self.level_limitX = -1000
        self.level_limitY = -300

        self.startX = 125
        self.startY = 275

        # [length, height, x, y]
        level = [[1100, 30, 0, 400],
                 ]

        nextLvl = [[40, 60, 1050, 340],
                   ]

        # enemy triangles
        enemies = [[35, 35, 400, 365],
                   [35, 35, 450, 365],
                   [35, 35, 500, 365],
                   [35, 35, 600, 365],
                   [35, 35, 800, 200],
                   [35, 35, 800, 330],
                   [35, 35, 800, 365],
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

        for enemy in enemies:
            bady = EnemyTri(enemy[0], enemy[1])
            bady.rect.x = enemy[2]
            bady.rect.y = enemy[3]
            bady.player = self.player
            self.enemyList.add(bady)

class Level_07(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/backgrounds/bluebluepurple1080.png').convert()
        self.background.set_colorkey(BLACK)

        self.level_limitX = -1000
        self.level_limitY = -10000

        self.startX = 125
        self.startY = 125

        # [length, height, x, y]
        level = [[640, 35, 10, 200],
                 [35, 190, 10, 10],
                 [750, 35, 10, 10],

                 [35, 35, 760, 20],
                 [35, 35, 795, 30],
                 [35, 35, 830, 40],
                 [35, 35, 865, 50],
                 [35, 1000, 865, 85],

                 [35, 885, 650, 200],

                 [250, 35, 650, 6800],
                 ]

        nextLvl = [[35, 60, 760, 6740],
                   ]

        triangles = [[35, 35, 760, 200],
                     [35, 35, 760, 235],
                     [35, 35, 760, 270],
                     [35, 35, 760, 800],
                     [35, 35, 760, 1000],
                     [35, 35, 760, 1500],
                     [35, 35, 760, 1600],
                     [35, 35, 760, 1700],
                     [35, 35, 760, 1800],
                     [35, 35, 760, 1900],
                     [35, 35, 760, 2000],
                     [35, 35, 760, 2100],
                     [35, 35, 760, 2200],
                     [35, 35, 760, 2300],
                     [35, 35, 760, 3500],
                     [35, 35, 700, 6765],

                     [35, 35, 685, 500],
                     [35, 35, 830, 700],
                   ]

        # pink death on contact platforms/walls
        deathWall = [[35, 2000, 650, 1085],
                     [35, 450, 760, 3535],
                     [35, 2000, 865, 1085],

                     [35, 3715, 650, 3085],
                     [35, 2755, 760, 3985],
                     [35, 3715, 865, 3085],
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

        for tri in triangles:
            bady = EnemyTri(tri[0], tri[1])
            bady.rect.x = tri[2]
            bady.rect.y = tri[3]
            bady.player = self.player
            self.enemyList.add(bady)

        for wall in deathWall:
            bady = EnemyPlat(wall[0], wall[1])
            bady.rect.x = wall[2]
            bady.rect.y = wall[3]
            bady.player = self.player
            self.enemyList.add(bady)

# placeholder level till further development, unbeatable
class Level_08(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load('assets/backgrounds/purplefinal.png').convert()
        self.background.set_colorkey(BLACK)

        self.level_limitX = -100
        self.level_limitY = -100

        self.startX = 140
        self.startY = 200

        # [length, height, x, y]
        level = [[550, 30, 125, 400],
                 ]

        nextLvl = [[40, 60, 400, 340],
                   ]

        enemies = [[35, 35, 365, 365],
                   [35, 35, 440, 365],
                   [35, 35, 402.5, 304],
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

        for enemy in enemies:
            bady = EnemyTri(enemy[0], enemy[1])
            bady.rect.x = enemy[2]
            bady.rect.y = enemy[3]
            bady.player = self.player
            self.enemyList.add(bady)

# main procedure
def main():

    # mixer pre initialized in order to fix audio delay on keypress
    pygame.mixer.pre_init(44100, -16, 2, 1024)

    # initializations and declarations
    pygame.init()
    pygame.mixer.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quebe")
    icon = pygame.image.load('assets/backgrounds/52favcropped.png')
    pygame.display.set_icon(icon.convert())
    player = Player()

    # create list of all current levels in order
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    level_list.append(Level_04(player))
    level_list.append(Level_05(player))
    level_list.append(Level_06(player))
    level_list.append(Level_07(player))
    level_list.append(Level_08(player))

    current_level_num = 0
    current_level = level_list[current_level_num]

    active_sprite_list = pygame.sprite.Group()

    player.level = current_level
    player.rect.x = current_level.startX
    player.rect.y = current_level.startY
    active_sprite_list.add(player)

    # background music
    pygame.mixer.music.load('assets/music/jhElegiac.ogg')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    music = True

    # flags
    done = False
    paused = False
    grav = True

    fpsClock = pygame.time.Clock()

# restarts the current level w/ camera reset
    def restart():
        player.stop()
        current_level.shiftWorldX(-current_level.world_shiftX)
        current_level.shiftWorldY(-current_level.world_shiftY)
        player.rect.x = current_level.startX
        player.rect.y = current_level.startY

# creates the menu and displays
    def menu():
        fontObjR = pygame.font.Font("assets/fonts/Raleway-Regular.ttf", 32)
        fontObjL = pygame.font.Font("assets/fonts/Raleway-Light.ttf", 20)

        textSurfP = fontObjR.render("Paused", True, WHITE)
        textRectP = textSurfP.get_rect()
        textRectP.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/15))

        textSurfQ = fontObjL.render("Press 'q' to Quit", True, WHITE)
        textRectQ = textSurfQ.get_rect()
        textRectQ.left = ((SCREEN_WIDTH/15))

        textSurfF1 = fontObjL.render("Press 'F1' for Help", True, WHITE)
        textRectF1 = textSurfF1.get_rect()
        textRectF1.right = ((SCREEN_WIDTH/15)*14)

        textSurfM = fontObjL.render("Press 'm' to Toggle Music", True, WHITE)
        textRectM = textSurfM.get_rect()
        textRectM.bottomleft = ((SCREEN_WIDTH/15), ((SCREEN_HEIGHT/15)*14))

        screen.blit(textSurfP, textRectP)
        screen.blit(textSurfQ, textRectQ)
        screen.blit(textSurfF1, textRectF1)
        screen.blit(textSurfM, textRectM)

        pygame.display.update()

# creates in-game help menu and displays
    def help():
        fontObjR = pygame.font.Font("assets/fonts/Raleway-Regular.ttf", 32)
        fontObjL = pygame.font.Font("assets/fonts/Raleway-Light.ttf",20)

        textSurf1 = fontObjR.render("Help", True, WHITE)
        textRect1 = textSurf1.get_rect()
        textRect1.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/15))

        textSurf2 = fontObjL.render("You are Quebe. You must get to the White Door. What awaits at the end?",
                                    True, WHITE)
        textRect2 = textSurf2.get_rect()
        textRect2.left = ((SCREEN_WIDTH/15))
        textRect2.top = ((SCREEN_HEIGHT/20)*3)

        textSurf3 = fontObjL.render("Move/Jump:     Arrow Keys or WASD", True, WHITE)
        textRect3 = textSurf3.get_rect()
        textRect3.left = ((SCREEN_WIDTH/15))
        textRect3.top = ((SCREEN_HEIGHT/20)*5)

        textSurf4 = fontObjL.render("Menu/Pause:    ESC", True, WHITE)
        textRect4 = textSurf4.get_rect()
        textRect4.left = ((SCREEN_WIDTH/15))
        textRect4.top = ((SCREEN_HEIGHT/20)*6)

        textSurf5 = fontObjL.render("Restart Level:     r", True, WHITE)
        textRect5 = textSurf5.get_rect()
        textRect5.left = ((SCREEN_WIDTH/15))
        textRect5.top = ((SCREEN_HEIGHT/20)*7)

        textSurf6 = fontObjL.render("Quit:                     q", True, WHITE)
        textRect6 = textSurf6.get_rect()
        textRect6.left = ((SCREEN_WIDTH/15))
        textRect6.top = ((SCREEN_HEIGHT/20)*8)

        textSurf7 = fontObjL.render("Toggle Music:    m", True, WHITE)
        textRect7 = textSurf7.get_rect()
        textRect7.left = ((SCREEN_WIDTH/15))
        textRect7.top = ((SCREEN_HEIGHT/20)*9)

        textSurf8 = fontObjL.render("Cheat - Skip to Next Level:         TAB", True, WHITE)
        textRect8 = textSurf8.get_rect()
        textRect8.left = ((SCREEN_WIDTH/15))
        textRect8.top = ((SCREEN_HEIGHT/20)*11)

        textSurf9 = fontObjL.render("Cheat - Toggle Jump Mode:       j", True, WHITE)
        textRect9 = textSurf9.get_rect()
        textRect9.left = ((SCREEN_WIDTH/15))
        textRect9.top = ((SCREEN_HEIGHT/20)*12)

        bckgnd = pygame.image.load('assets/backgrounds/purple800x600.jpg').convert()
        screen.blit(bckgnd, [0, 0])
        screen.blit(textSurf1, textRect1)
        screen.blit(textSurf2, textRect2)
        screen.blit(textSurf3, textRect3)
        screen.blit(textSurf4, textRect4)
        screen.blit(textSurf5, textRect5)
        screen.blit(textSurf6, textRect6)
        screen.blit(textSurf7, textRect7)
        screen.blit(textSurf8, textRect8)
        screen.blit(textSurf9, textRect9)

        pygame.display.update()

    # main game loop, terminates on quit command
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # toggle pause
                if event.key == pygame.K_ESCAPE:
                    if paused == False:
                        paused = True
                        menu()
                    elif paused == True:
                        paused = False
                # player movements
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.goLeft()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.goRight()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if grav == True:
                        player.jump()
                    else:
                        player.goUp()  # when jump cheat is on
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if grav == False:
                        player.goDown()
                # restart level
                if event.key == pygame.K_r:
                    restart()
                # when in menu
                if paused == True:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F1:
                        help()
                # toggle music
                if event.key == pygame.K_m:
                    if music == True:
                        pygame.mixer.music.pause()
                        music = False
                    else:
                        pygame.mixer.music.unpause()
                        music = True
                # toggle jump cheat
                if event.key == pygame.K_j:
                    if grav == True:
                        grav = False
                    else:
                        grav = True

            if event.type == pygame.KEYUP:
                # end player movements
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
        # only update if not paused
        #BUG: jump sound plays while paused
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

            # checks collision from triangle enemies / death walls
            enemy_hit_list = pygame.sprite.spritecollide(player, player.level.enemyList, False)
            for enemy in enemy_hit_list:
                restart()

            # screen scrolling
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

            # end of current level boundaries, restart if out of bounds
            current_positionX = player.rect.x + current_level.world_shiftX
            current_positionY = player.rect.y + current_level.world_shiftY
            if current_positionX < current_level.level_limitX:
                restart()
            if current_positionY < current_level.level_limitY:
                restart()

            # draws to screen surface
            current_level.draw(screen)
            active_sprite_list.draw(screen)

            # refresh rate limiter
            fpsClock.tick(FPS)
            # flips entire surface to screen
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()