import pygame
import time
import random

pygame.init()

# crash_sound = pygame.mixer.Sound('crash.wav')
# pygame.mixer.music.load('song.wav')

display_width = 900
display_height = 900

black = (0, 0, 0)
white = (255, 255, 255)
red = (100, 0, 0)
yellow = (100, 100, 0)
green = (0, 100, 0)
blue = (0, 0, 100)

bright_red = (255, 0, 0)
bright_yellow = (255, 255, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Simon')
clock = pygame.time.Clock()

score = 0
square_seq = random.choice('rgby')
square_cur = square_seq[0]
square_place = 0
square_blink = ''

r_square = {'x': 225,
            'y': 125,
            'w': 200,
            'h': 200,
            'ic': red,
            'ac': bright_red,
            'code': 'r'}
b_square = {'x': 475,
            'y': 125,
            'w': 200,
            'h': 200,
            'ic': blue,
            'ac': bright_blue,
            'code': 'b'}
g_square = {'x': 225,
            'y': 375,
            'w': 200,
            'h': 200,
            'ic': green,
            'ac': bright_green,
            'code': 'g'}
y_square = {'x': 475,
            'y': 375,
            'w': 200,
            'h': 200,
            'ic': yellow,
            'ac': bright_yellow,
            'code': 'y'}

squares = (r_square, b_square, g_square, y_square)


def current_score(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def fail_game():

    global score
    global square_seq
    global square_cur
    global square_place
    global square_blink

    score = 0
    square_seq = random.choice('rgby')
    square_cur = square_seq[0]
    square_place = 0
    square_blink = ''

#    pygame.mixer.music.stop()
#    pygame.mixer.Sound.play(crash_sound)

    gameDisplay.fill(white)
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("You Lose", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        button("Play Again", 150, 700, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 700, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def square(x, y, w, h, ic, ac, code):

    global square_blink

    if square_blink == code:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))


def advance_color():

    global square_seq
    global square_cur
    global square_place
    global score

    if square_place + 1 == len(square_seq):
        square_seq += random.choice('rgby')
        square_place = 0
        score += 1
        square_cur = square_seq[0]
        game_loop()
    else:
        square_place += 1
        square_cur = square_seq[square_place]


def button(msg, x, y, w, h, ic, ac, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()


def check_click(x, y, w, h, ic, ac, code):
    mouse = pygame.mouse.get_pos()
    if (x + w > mouse[0] > x and y + h > mouse[1] > y):
        return True


def game_intro():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Simon", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 700, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 700, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_loop():

    global square_blink
    global square_cur
    square_blink = None

#    pygame.mixer.music.play(-1)

    gameDisplay.fill(white)
    current_score(score)

    for item in squares:
        square(*item.values())

    pygame.display.update()
    time.sleep(1)
    do_blink()
    square_blink = None

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.MOUSEBUTTONUP:
                    for item in squares:
                        if check_click(*item.values()):
                            if item['code'] == square_cur:
                                advance_color()
                            else:
                                fail_game()

        gameDisplay.fill(white)
        current_score(score)

        for item in squares:
            square(*item.values())

        pygame.display.update()
        clock.tick(60)


def do_blink():

    global square_seq
    global square_cur
    global square_place
    global square_blink

    for item in square_seq:
        square_blink = item
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(white)
        current_score(score)

        for item in squares:
            square(*item.values())
        pygame.display.update()
        time.sleep(1)

        square_blink = None
        for item in squares:
            square(*item.values())
        pygame.display.update()
        time.sleep(0.2)


game_intro()
quitgame()
