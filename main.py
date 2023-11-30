from random import randint
from math import sqrt
import pygame


class Ball:
    def __init__(self, disp, cords, dispsize, fps, other_balls, rad=15, colour=None,
                 kk=0.8, yvel=0, xvel=0, gravity=9.806):
        global c
        self.disp = disp
        self.x, self.y = self.cords = cords
        self.rad = rad
        self.colour = colour

        self.yvel = yvel
        self.xvel = xvel

        self.balls = other_balls
        self.dispsize = dispsize
        self.fps = fps
        self.kk = kk
        self.colls = list()
        self.lx = 0
        self.ly = 0
        self.dodraw = True

        if not colour:
            self.colour = randint(0, 255), randint(0, 255), randint(0, 255)
        else:
            self.colour = colour

        self.gravp = gravity

    def draw(self):
        if self.dodraw:
            pygame.draw.circle(surface=self.disp, color=self.colour, center=self.cords, radius=self.rad)
        else:
            del self

    def render(self):
        self.other_balls_collide()
        self.change_cords()
        self.upcord()
        self.draw()

    def upcord(self):
        self.cords = (self.x, self.y)

    def bounce(self):
        if abs(self.yvel * self.kk) >= 10:
            self.yvel = -(self.yvel * self.kk)
            self.xvel = self.xvel * self.kk
        else:
            self.yvel = 0
            self.xvel = self.xvel * self.kk

    def bounce_wall(self):
        self.yvel = self.yvel * self.kk
        self.xvel = -(self.xvel * self.kk)

    def collided(self, cords, er=0):
        outl = []
        for nut in self.balls:

            if nut != self:

                ox, oy = nut.cords
                sx, sy = cords

                xdiff = abs(ox - sx)
                ydiff = abs(oy - sy)

                distance = sqrt(xdiff**2 + ydiff**2)
                # print(distance, (self.rad + nut.rad))
                if distance + er <= (self.rad + nut.rad):
                    outl.append(nut)
        self.colls = outl

    def other_balls_collide(self):
        # grab your left nut, make right one jealous!
        self.collided(self.cords)
        collided_balls = self.colls
        if collided_balls:
            for ball in collided_balls:
                if self.lx == 0 and self.ly == 0:
                    self.dodraw = False
                    # ox, oy = ball.cords
                    # sx, sy = self.cords
                    # xdiff = ox - sx
                    # ydiff = oy - sy

                olvx = self.xvel
                olvy = self.yvel
                self.xvel = -self.xvel * self.kk / 2
                self.yvel = -self.yvel * self.kk / 2

                ball.xvel += olvx * ball.kk / 2
                ball.yvel += olvy * ball.kk / 2

                self.x = self.lx
                self.y = self.ly




















    def change_cords(self):

        if self.y + self.rad <= self.dispsize[1]:
            self.gravity()

        else:
            if self.yvel > 0:
                self.y = self.dispsize[1] - self.rad
                self.bounce()

        newy = self.y + self.yvel / self.fps
        newx = self.x + self.xvel / self.fps

        self.collided((newx, newy))

        if self.xvel != 0 or (self.yvel != 0 or str(self.yvel) != str(self.gravp)):

            if newy + self.rad <= self.dispsize[1] and newy - self.rad > 0:
                self.ly = self.y
                self.y = newy

            else:
                if not newy + self.rad <= self.dispsize[1]:
                    self.ly = self.y
                    self.y = self.dispsize[1] - self.rad
                    self.bounce()
                elif newy - self.rad <= 0:
                    self.ly = self.y
                    self.y = self.rad
                    self.bounce()

            if newx + self.rad <= self.dispsize[0] and newx - self.rad > 0:
                self.lx = self.x
                self.x = newx

            else:
                if not newx + self.rad <= self.dispsize[0]:
                    self.lx = self.x
                    self.x = self.dispsize[0] - self.rad
                    self.bounce_wall()
                elif newx - self.rad <= 0:
                    self.lx = self.x
                    self.x = self.rad
                    self.bounce_wall()

    def gravity(self):
        self.yvel += self.gravp


if __name__ == "__main__":
    pygame.init()

    size = (600, 600)
    mscr = pygame.display.set_mode(size)

    run = True

    frps = 300

    clock = pygame.time.Clock()

    balls = []

    power = 3

    while run:
        mscr.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                # print(keys)
                if keys[pygame.K_SPACE]:
                    balls = []

                elif keys[pygame.K_LEFT]:
                    balls.append(Ball(mscr, pygame.mouse.get_pos(), size, frps, balls, xvel=-250 * power))

                elif keys[pygame.K_RIGHT]:
                    balls.append(Ball(mscr, pygame.mouse.get_pos(), size, frps, balls, xvel=250 * power))

                elif keys[pygame.K_UP]:
                    balls.append(Ball(mscr, pygame.mouse.get_pos(), size, frps, balls, yvel=-250 * power))

                elif keys[pygame.K_LEFT]:
                    balls.append(Ball(mscr, pygame.mouse.get_pos(), size, frps, balls, yvel=-250 * power))

                elif keys[pygame.K_DOWN]:
                    balls.append(Ball(mscr, pygame.mouse.get_pos(), size, frps, balls, yvel=250 * power))

                elif keys[pygame.K_1]:
                    power = 1
                elif keys[pygame.K_2]:
                    power = 2
                elif keys[pygame.K_3]:
                    power = 3
                elif keys[pygame.K_4]:
                    power = 4
                elif keys[pygame.K_5]:
                    power = 5
                elif keys[pygame.K_6]:
                    power = 6
                elif keys[pygame.K_7]:
                    power = 7
                elif keys[pygame.K_8]:
                    power = 8
                elif keys[pygame.K_9]:
                    power = 9
                elif keys[pygame.K_0]:
                    power = 0

        for ball in balls:
            ball.render()

        pygame.display.flip()
        clock.tick(frps)
