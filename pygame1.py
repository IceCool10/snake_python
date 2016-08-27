import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Slither')
icon = pygame.image.load('apple.png') #the top left icon ( 32 x 32 px )
pygame.display.set_icon(icon) # add the image

img = pygame.image.load("snakehead.png")
appleimg = pygame.image.load("apple.png")

pygame.display.update()



clock = pygame.time.Clock() #clock object

AppleThickness = 30
block_size = 20
FPS = 15

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25) # 25 --> Size
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        message_to_screen("Paused", white, -100, "large")
        message_to_screen("Press C to continue or Q to quit", white, 25, "small")
        pygame.display.update()
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: " + str(score) , True, white)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))# / 10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height - AppleThickness))# / 10.0) * 10.0
    return randAppleX, randAppleY


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


        gameDisplay.fill(black)

        message_to_screen("Welcome to Slither", green, -100, "large")
        message_to_screen("The objective is to eat read apples", white, -30)
        message_to_screen("The more applesyou eat, the longer you get", white, 10)
        message_to_screen("If you run into yourself or the edges you DIE!", white, 50)
        message_to_screen("Press C to play, P to pause or Q to quit", white, 180)
        pygame.display.update()

        clock.tick(15)


def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [ XnY[ 0 ], XnY[ 1 ], block_size, block_size])


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)

    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    gameExit = False
    gameOver = False
    global direction
    direction = 'right'

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("Game over",red, y_displace = -50, size = "large")
            message_to_screen("press C to play again or Q to quit", white, 50, size = "medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if lead_x_change != block_size:
                        lead_x_change = -block_size
                        lead_y_change = 0
                        direction = "left"
                    else:
                        continue
                elif event.key == pygame.K_RIGHT:
                    if lead_x_change != -block_size:
                        lead_x_change = block_size
                        lead_y_change = 0
                        direction = "right"
                    else:
                        continue
                elif event.key == pygame.K_UP:
                    if lead_y_change != block_size:
                        lead_y_change = -block_size
                        lead_x_change = 0
                        direction = "up"
                    else:
                        continue
                elif event.key == pygame.K_DOWN:
                    if lead_y_change != -block_size:
                        lead_y_change = block_size
                        lead_x_change = 0
                        direction = "down"
                    else:
                        continue
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_ESCAPE:
                    pause()
            #print(event)
        if lead_x > display_width or lead_x < 0 or lead_y > display_height or lead_y < 0:
            gameOver = True
        lead_x += lead_x_change
        lead_y += lead_y_change


        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or  lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
        gameDisplay.fill(black)


        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        #pygame.draw.rect(where to draw, color, [positionX, positionY, length, width]
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        snake(block_size, snakeList)

        #pygame.draw.rect(gameDisplay, red, [400,300,10,10])
        #gameDisplay.fill(red, rect=[200, 200, 15, 15])

        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])



        score(snakeLength - 1)

        pygame.display.update()
        clock.tick(FPS)


    pygame.quit()
    quit()


game_intro()
gameLoop()