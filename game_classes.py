from __future__ import annotations
import pygame as pg
from random import choice
import win32api
from math import sin, cos
from math import radians as rad

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

    @staticmethod
    def getMonitorRefreshRate():
        device = win32api.EnumDisplayDevices()
        settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
        return int(getattr(settings, 'DisplayFrequency'))

win = Window(1920, 1080)

class Pad(pg.Rect):
    pads: list[Pad] = []
    DEFAULT_SPEED = 5
    SIZE = (15, 200)

    def __init__(self, coords: tuple, dimensions: tuple = SIZE, movement_keys: tuple[int, int] | None = None, color: tuple = WHITE, speed = DEFAULT_SPEED):
        super().__init__(coords, dimensions)
        self.color = color
        self.speed = speed
        self.movement_keys = movement_keys
        Pad.pads.append(self)

    def handle_movement(pressed_keys):
        for p in Pad.pads:
            if pressed_keys[p.movement_keys[0]]:
                if p.top > 0:
                    p.y -= p.speed
                else:
                    p.top = 1
            
            if pressed_keys[p.movement_keys[1]]:
                if p.bottom < win.res("h"):
                    p.y += p.speed
                else:
                    p.bottom = win.res("h")-1

    @staticmethod
    def get_pad(r: pg.Rect, color: tuple = WHITE):
        newpad = Pad((r.x, r.y), Pad.SIZE, color)
        return newpad

class Ball(pg.Rect):
    balls: list[Ball] = []
    DEFAULT_STARTING_SPEED = 3
    DEFAULT_ACCELLERATION = 0.20
    DEFAULT_SIZE = (15, 15)

    @staticmethod
    def angleRng():
        random_angle = choice([45, 135, 225, 315])
        return random_angle

    def __init__(self, pos = win.center, size = DEFAULT_SIZE, starting_angle = angleRng(), speed = DEFAULT_STARTING_SPEED, accelleration = DEFAULT_ACCELLERATION):
        super().__init__(pos, size)
        self.speed = speed
        self.starting_angle = starting_angle
        self.starting_angle_x = cos(rad(starting_angle))
        self.starting_angle_y = self.starting_angle_x
        self.direction = pg.math.Vector2(self.starting_angle_x, self.starting_angle_y)
        self.accelleration = accelleration
        Ball.balls.append(self)

    def handle_movement():
        for ball in Ball.balls:
            ball.x += ball.direction.x * ball.speed
            ball.y += ball.direction.y * ball.speed

            if ball.y <= 1 or ball.y >= win.res("h") -1:
                stickyfix = -1 * ball.speed if ball.direction.y > 0 else 1 * ball.speed
                ball.y = ball.y + stickyfix
                ball.direction.y *= -1
            for pad in Pad.pads:
                if pad.colliderect(ball):
                    ball.speed += ball.accelleration
                    ball.x += 1 if ball.direction.x < 0 else -1
                    ball.direction.x *= -1

class Border(pg.Rect):
    BORDER_THICKNESS = 3
    def __init__(self, coords: tuple[int, int], dimensions: tuple[int, int], color: tuple[int, int, int]):
        super().__init__(coords, dimensions)
        self.color = color

class Text():
    pg.font.init()
    MAIN_FONT = pg.font.Font("./assets/CascadiaCode.ttf", 48)
    TEXT_OFFSET1 = (40,40)
    TEXT_OFFSET2 = (win.res("w") - TEXT_OFFSET1[0] * 4, TEXT_OFFSET1[1])
    TEXT_OFFSET_BALLSPEED = (win.res("w")/2-(TEXT_OFFSET1[0]*2), TEXT_OFFSET1[1])

    def renderText(text, color: tuple = WHITE, getRectangle = False, font = MAIN_FONT):
        rendered_text = font.render(str(text), True, color)
        if getRectangle:
            return rendered_text, rendered_text.get_rect()
        else:
            return rendered_text

class Graphics:

    # background
    bg = pg.transform.scale(pg.image.load("./assets/city.jpg"), win.res())

    # borders
    border1 = Border((0,0), (Border.BORDER_THICKNESS, win.res("h")), BLUE)
    border2 = Border((win.res("w") - Border.BORDER_THICKNESS,0), (Border.BORDER_THICKNESS, win.res("h")), BLUE)