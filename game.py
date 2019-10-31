import pygame, random, sys, time
from pygame.locals import *

#time at which more arrows will appear
moreArrows = 7

arrowMinSize = 8
arrowMaxSize = 15
arrowMinSpeed = 5
arrowMaxSpeed = 8
FPS = 30

#players moving rate/speed
movingRate = 5
Clock = pygame.time.Clock()
highestTime = 1000
current1 = 0
#start time
start = 0
#colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,180,0)
intro_colour = (64,105,150)
bg = (5,95,94)
orange = (255,83,0)

time1 = 0
#dimensions
display_width = 800
display_height = 600

#end game
def endgame():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    #pygame.time.set_ticks(0)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                endgame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    endgame()
                return


def arrowHitPlayer(playerRect,arrows):
    for a in arrows:
        if playerRect.colliderect(a['rect']):
            pygame.time.delay(150)
            return True
    return False

def playerCaptureFlag(playerRect,flagRect):
        if playerRect.colliderect(flagRect):
            pygame.time.delay(1000)
            return True
        return False
    


#message on the screen
def message_to_screen(text,font,surface,x,y,color):
    #text rect where we will put the text
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    #put text on screen
    surface.blit(textobj, textrect)


pygame.init()
#surface
gameDisplay = pygame.display.set_mode((display_width,display_height))
#title of game
pygame.display.set_caption('Dodge')


#set up font
font = pygame.font.SysFont(None, 42)

#set up images
myPlayer = pygame.image.load('dot.png')
playerRect = myPlayer.get_rect()
arrowsImage = pygame.image.load('arrows.png')
flag = pygame.image.load('flag.png')
flagRect = flag.get_rect()
#screen rect to keep player within the boundary
screenRect = gameDisplay.get_rect()
pygame.draw.rect(gameDisplay,(0,0,0), playerRect)

#display start screen
message_to_screen('Dodge',font,gameDisplay,(display_width/3+(100)),(display_height/3),red)
message_to_screen('Capture the flag as quickly as you can', font,gameDisplay, (display_width/3)-85,(display_height/3+(60)),red)
message_to_screen('Press a key to start', font,gameDisplay, (display_height/3+80),(display_width/3)+70,red)
pygame.display.update()
waitForPlayerToPressKey()


while True:
    
    # set up the start of the game
    arrows = []
    score = 0
    #default player position
    playerRect.topleft = (display_width/2, (display_height)-50)
    #flagposition
    flagRect.topleft = (750, display_height-600)
    moveLeft = moveRight = moveUp = moveDown = False

    #gameloop
    #global start
    start = time.time() 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                endgame()
            
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    endgame()
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

           
        # Add arrow to top of screen
        arrowSize = random.randint(arrowMinSize,arrowMaxSize)
        newArrow = {'rect': pygame.Rect(random.randint(0, display_width-arrowSize),0-arrowSize,arrowSize,arrowSize),
                        'speed': random.randint(arrowMinSpeed, arrowMaxSpeed),
                        'surface': pygame.transform.scale(arrowsImage, (arrowSize, arrowSize)),
                        } 
                     
        arrows.append(newArrow)
         #new arrow item
        current = time.time()
        current1 += 7
        if current1 == moreArrows:
            current1 = 0
            arrowSize = random.randint(arrowMinSize,arrowMaxSize)
            #(x,y,width,height)
            newArrow = {'rect': pygame.Rect(random.randint(0, display_width-arrowSize),0-arrowSize,arrowSize,arrowSize),
                        'speed': random.randint(arrowMinSpeed, arrowMaxSpeed),
                        'surface': pygame.transform.scale(arrowsImage, (arrowSize, arrowSize)),
                        } 
                     
            arrows.append(newArrow)

        #moving the player
        if moveLeft and playerRect.left > 0:
            #move_ip(x,y)
            playerRect.move_ip(-1* movingRate, 0)
        if moveRight and playerRect.right > 0:
            playerRect.move_ip(movingRate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1* movingRate)
        if moveDown and playerRect.bottom > 0:
            playerRect.move_ip(0,movingRate)

        

        #moving the arrows down
        for a in arrows:
            a['rect'].move_ip(0, a['speed'])

            
        # delete arrows that have fallen past
        for a in arrows[:]:
            if a['rect'].top > display_height:
                arrows.remove(a)

        #change bg colour 
        gameDisplay.fill(white)
        #if pygame.time.get_ticks()>10000 and pygame.time.get_ticks() < 20000:
            #gameDisplay.fill(black)
        #else: gameDisplay.fill(white)
        #keep player within the screen
        playerRect.clamp_ip(screenRect)
        
        #draw player's rectangle
        gameDisplay.blit(myPlayer, playerRect)
        #draw flag
        gameDisplay.blit(flag,flagRect)

       
        #if player wins
        if playerCaptureFlag(playerRect, flagRect):
            gameDisplay.fill(black)
            end = time.time()
            time1 = end-start
            message_to_screen('Congratulations! You captured the flag in ' + str(round((time1),2)) + ' seconds', font, gameDisplay, 10,display_height/3, green)
            message_to_screen('Your score:' + str(round((time1),2)) + ' seconds',font, gameDisplay, 10, 0,green)
            message_to_screen('Press any key to play again', font ,gameDisplay,(display_width/2-160), (display_height/2), orange)
            if  time1 < highestTime :
                highestTime = time1 #new high score
                message_to_screen('New high score!', font ,gameDisplay,(display_width/2-100), (display_height/2 - 150), orange)
                message_to_screen('Top score: ' + str(round((highestTime),2)) + ' seconds',font, gameDisplay, 10,40,green)
            
                
            break
            
            
        #draw each arrow
        for a in arrows:
            gameDisplay.blit(a['surface'], a['rect'])

        pygame.display.update()

                
        #check for collision between the player and arrow
        if arrowHitPlayer(playerRect, arrows):
            gameDisplay.fill(black)
            message_to_screen('GAME OVER',font, gameDisplay, (display_width/3+40), (display_height/3), orange)
            message_to_screen('Press a key to play again', font ,gameDisplay,(display_width/2-160), (display_height/2), orange)
            break
        #slows the game down
        Clock.tick(FPS)
        

        

    #Game over screen
    print(pygame.time.get_ticks())
    pygame.display.flip()
    pygame.display.update()
    waitForPlayerToPressKey()
    
        
    


