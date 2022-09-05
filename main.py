from game_classes import *

# TODO
# fix ball angle, dat shit too slow

# display stuff
screen = pg.display.set_mode(win.res(), pg.FULLSCREEN)
clk = pg.time.Clock()
refresh_rate = Window.getMonitorRefreshRate()
pg.mouse.set_visible(False)
# pg.font.init()

# pads
pad1 = Pad((0, win.res("h")/2), movement_keys=[pg.K_w, pg.K_s])
pad2 = Pad((win.res("w") - Pad.SIZE[0], win.res("h")/2), movement_keys=[pg.K_UP, pg.K_DOWN])

# ball
ball = Ball()

class Game():

    run = True
    player1_score = 0
    player2_score = 0
    level = 1

    offsets = {
        Graphics.bg: (0,0),
        player1_score: Text.TEXT_OFFSET1,
        player2_score: Text.TEXT_OFFSET2,
        ball.speed: Text.TEXT_OFFSET_BALLSPEED
    }  

    @staticmethod
    def reset(dontFlipBall=False):
        for ball in Ball.balls:
            ball.x, ball.y = win.center
            ball.speed = ball.DEFAULT_STARTING_SPEED
            if not dontFlipBall:
                ball.direction.x *= -1

    @staticmethod
    def handle_movements_and_keys():

        # quitting should be handled first
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Game.run = False
                break

        pressed_keys = pg.key.get_pressed()
        Pad.handle_movement(pressed_keys) # also handles keypresses for pads
        Ball.handle_movement()
        Game.get_score()

        if pressed_keys[pg.K_r]:
            Game.reset(True)
        if pressed_keys[pg.K_ESCAPE]:
            Game.run = False

    @staticmethod
    def get_score():
        for ball in Ball.balls:
            if ball.x <= 0:
                Game.player2_score += 1
                Game.reset()
                return
            elif ball.x >= win.res("w"):
                Game.player1_score += 1
                Game.reset()
                return

    # this should have been in the Graphics class, but I couldn't access some elements that way
    toggle_fps = False
    @staticmethod
    def draw_all():
        # needs to be done manually like this, to preserve order
        screen.blit(Graphics.bg, (0,0))
        pg.draw.rect(screen, RED, Graphics.border1)
        pg.draw.rect(screen, RED, Graphics.border2)
        pg.draw.rect(screen, WHITE, pad1)
        pg.draw.rect(screen, WHITE, pad2)
        pg.draw.rect(screen, GREEN, ball)
        screen.blit(Text.renderText(Game.player1_score, WHITE), Text.TEXT_OFFSET1)
        screen.blit(Text.renderText(Game.player2_score, WHITE), Text.TEXT_OFFSET2)
        screen.blit(Text.renderText("{:.2f}".format(ball.speed) + " m/s", WHITE), Text.TEXT_OFFSET_BALLSPEED)

        if pg.key.get_pressed()[pg.K_f]:
                Game.toggle_fps ^= True
                if Game.toggle_fps:
                    screen.blit(Text.renderText(f"FPS: {clk.get_fps().__round__()}"), (20, win.res("h") - 60))
                    Game.toggle_fps = False

# debug
DEBUG = False
def draw_debug_info():
    debug_font = pg.font.Font("./assets/CascadiaCode.ttf", 36)
    screen.blit(Text.renderText(f"{ball.direction.xy}", font=debug_font), (win.res("w")/8, 20)) #debug
    screen.blit(Text.renderText(f"{ball.starting_angle_x}", font=debug_font), (win.res("w")/8, win.res("h") - 50)) #debug
    screen.blit(Text.renderText(f"{(ball.speed * ball.direction.x).__round__(2)}, {(ball.speed * ball.direction.y).__round__(2)}", font=debug_font), (win.res("w")*(5/8), 20)) #debug


def main_loop():

    while Game.run:
        clk.tick(refresh_rate)

        Game.handle_movements_and_keys()
        Game.draw_all()        
        if DEBUG: draw_debug_info()
        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main_loop()