import pygame
from random import randint


class Ball:
    def __init__(self, disp, cords, dispsize, fps, rad=15, colour=(255, 0, 0), kk=0.85):
        self.disp = disp
        self.x, self.y = self.cords = cords
        self.rad = rad
        self.colour = colour
        self.vel = 0
        self.dispsize = dispsize
        self.fps = fps
        self.kk = kk

        self.gravp = 9.806

    def draw(self):
        pygame.draw.circle(surface=self.disp, color=self.colour, center=self.cords, radius=self.rad)

    def render(self):
        self.change_cords()
        self.upcord()
        self.draw()

    def upcord(self):
        self.cords = (self.x, self.y)

    def bounce(self):
        self.vel = -(self.vel * self.kk)

    def change_cords(self):
        if self.y + self.rad <= self.dispsize[1]:
            self.change_vel()
            newy = self.y + self.vel
            if newy + self.rad <= self.dispsize[1]:
                self.y = newy
            else:
                self.y = self.dispsize[1] - self.rad
                self.bounce()

        else:
            self.y = self.dispsize[1] - self.rad
            self.bounce()

    def change_vel(self):
        self.vel += self.gravp * (1 / self.fps)


if __name__ == "__main__":
    pygame.init()

    size = (600, 600)
    mscr = pygame.display.set_mode(size)

    run = True

    frps = 75

    circle = Ball(mscr, (300, 300), size, frps)

    clock = pygame.time.Clock()

    balls = []

    while run:
        mscr.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = (randint(0, 255), randint(0, 255), randint(0, 255))
                balls.append(Ball(mscr, event.pos, size, frps, colour=color))

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    balls = []
                    print('cleared')

        for ball in balls:
            ball.render()

        pygame.display.flip()
        clock.tick(frps)
