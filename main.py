import pygame as pg
import win32api
from random import choice
from math import sin, cos
from math import radians as rad
import time

# TODO
# write ball as class
# use git

# colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Window:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.center = width/2, height/2
        self.centerwidth = width/2
        self.centerheight = height/2

    def res(self, value=""):
        if value == "w":
            return self.width
        elif value == "h":
            return self.height
        else:
            return (self.width, self.height)

def getMonitorRefreshRate():
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    return int(getattr(settings, 'DisplayFrequency'))

class Pad(pg.Rect):
    DEFAULT_SPEED = 5
    SIZE = (15, 200)
    BONUS_SPEED = 2 # if the ball speed is higher than this, pads get bigger
    BONUS = 100

    def __init__(self, coords: tuple, dimensions: tuple = SIZE, color: tuple = WHITE, speed = DEFAULT_SPEED):
        super().__init__(coords, dimensions)
        self.color = color
        self.speed = speed
    
    @staticmethod
    def get_pad(r: pg.Rect, color: tuple = WHITE):
        newpad = Pad((r.x, r.y), Pad.SIZE, color)
        return newpad


# game functions



# window
win = Window(1920, 1080)
screen = pg.display.set_mode(win.res(), pg.FULLSCREEN)
clk = pg.time.Clock()

refresh_rate = getMonitorRefreshRate()

# background
bg = pg.transform.scale(pg.image.load("./assets/city.jpg"), win.res())

# pad

pad1 = Pad((0, win.res("h")/2))
pad2 = Pad((win.res("w") - Pad.SIZE[0], win.res("h")/2))
centerpad = Pad((win.res("w")/2, 0))

# borders
BORDER_THICKNESS = 3
border1 = pg.Rect((0,0), (BORDER_THICKNESS, win.res("h")))
border2 = pg.Rect((win.res("w") - BORDER_THICKNESS,0), (BORDER_THICKNESS, win.res("h")))

# ball
def angleRng():
    return choice([45, -45, 45+90, 45+180])

BALL_STARTING_SPEED = 3
ball_acceleration = 0.20
ball_speed = BALL_STARTING_SPEED
BALL_SIZE = (15, 15)
ball = pg.Rect(win.center, BALL_SIZE)
ball_starting_angle = rad(angleRng())
ball_startingspeed_x = cos(ball_starting_angle)
ball_startingspeed_y = sin(ball_starting_angle)

def reset(dontFlipBall=False):
    ball.x, ball.y = win.center
    global ball_speed
    ball_speed = BALL_STARTING_SPEED
    global speedup_clk
    speedup_clk = -1
    global n
    n = 1
    if dontFlipBall == False:
        ball_direction.x = -ball_direction.x

ball_direction = pg.math.Vector2(ball_startingspeed_x, ball_startingspeed_y)

# score
player1_score = 0
player2_score = 0

# font
pg.font.init()
MAIN_FONT = pg.font.Font("./assets/CascadiaCode.ttf", 48)
text_offset1 = (40,40)
text_offset2 = (win.res("w") - text_offset1[0] * 4, text_offset1[1])
text_offset_ballspeed = (win.res("w")/2-(text_offset1[0]*2), text_offset1[1])
def renderText(text, color: tuple = WHITE, getRectangle = False, font = MAIN_FONT):
    rendered_text = font.render(str(text), True, color)
    if getRectangle:
        return rendered_text, rendered_text.get_rect()
    else:
        return rendered_text

pg.mouse.set_visible(False)

def handle_keys():
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        if pad1.top > 0:
            pad1.y -= pad1.speed
        else:
            pad1.top = 1
    if keys[pg.K_s]:
        if pad1.bottom < win.res("h"):
            pad1.y += pad1.speed
        else:
            pad1.bottom = win.res("h")-1
    if keys[pg.K_UP]:
        if pad2.top > 0:
            pad2.y -= pad2.speed
        else:
            pad2.top = 1
    if keys[pg.K_DOWN]:
        if pad2.bottom < win.res("h"):
            pad2.y += pad2.speed
        else:
            pad2.bottom = win.res("h")-1
    if keys[pg.K_r]:
        reset(True)
    if keys[pg.K_ESCAPE]:
        global run
        run = False

def handle_centerpad():
    if centerpad.bottom < win.res("h"):
        centerpad.y += centerpad.speed
    else:
        centerpad.y -= 1
    if centerpad.top >= 0:
        centerpad.y -= centerpad.speed
    else:
        centerpad.y += 1

# debug
DEBUG = False
if DEBUG:
    global debug_font
    debug_font = pg.font.Font("./assets/CascadiaCode.ttf", 36)
def debug_info():

    screen.blit(renderText(f"{ball_direction.xy}", font=debug_font), (win.res("w")/8, 20)) #debug
    screen.blit(renderText(f"{(ball_speed * ball_direction.x).__round__(2)}, {(ball_speed * ball_direction.y).__round__(2)}", font=debug_font), (win.res("w")*(5/8), 20)) #debug
    screen.blit(renderText(f"FPS: {clk.get_fps().__round__()}", font=debug_font), (20, win.res("h") - 50)) #debug


bonus_given = False
run = True


while run:
    clk.tick(refresh_rate)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break

    # key handling
    handle_keys()
    
    # ball movement and collision
    ball.x += ball_direction.x * ball_speed
    ball.y += ball_direction.y * ball_speed

    if ball.y <= 1 or ball.y >= win.res("h") -1:
        stickyfix = -1 * ball_speed if ball_direction.y > 0 else 1 * ball_speed
        ball.y = ball.y + stickyfix
        ball_direction.y = -1*ball_direction.y
    if pad1.colliderect(ball) or pad2.colliderect(ball):
        ball_speed += ball_acceleration
        ball.x += 1 if pad1.colliderect(ball) else -1
        ball_direction.x = -1*ball_direction.x
    if ball.x <= 0:
        player2_score += 1
        reset()
    if ball.x >= win.res("w"):
        player1_score += 1
        reset()

    # drawing of the shit
    screen.blit(bg, (0,0))
    pg.draw.rect(screen, RED, border1)
    pg.draw.rect(screen, RED, border2)
    pg.draw.rect(screen, WHITE, pad1)
    pg.draw.rect(screen, WHITE, pad2)
    pg.draw.rect(screen, GREEN, ball)
    screen.blit(renderText(player1_score, WHITE), text_offset1)
    screen.blit(renderText(player2_score, WHITE), text_offset2)
    screen.blit(renderText("{:.2f}".format(ball_speed) + " m/s", WHITE), text_offset_ballspeed)
    if DEBUG: debug_info()

    pg.display.update()

pg.quit()