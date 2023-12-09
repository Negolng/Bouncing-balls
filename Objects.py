from Gravitron import Gravitron, BlackHole, Display
from random import randint
import pygame
import sys
import os

fps = 120

pygame.init()
screensize = (900, 900)
screen = pygame.display.set_mode(screensize)
dispy = Display(screen, screensize, fps, 0.001, 9.802, 0.1, 1)


def rand_col():
    return tuple((randint(0, 255), randint(0, 255), randint(0, 255)))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"АХ ТЫ СУКА! ГДЕ {fullname}, БЛЯТЬ?!?!!? ГДЕ?!?!?!\nAAAAAAAAAAAAAAA")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):
    __slots__ = ['display', 'x', 'y', 'rad', 'x_vel', 'y_vel', 'colour', 'bounce_c', 'others', 'gravy_objects']
    image = load_image('ball.png', -1)

    def __init__(self, display: Display, cords: tuple, radius: int, x_velocity: int | float, y_velocity: int | float,
                 grav_objects: list, other_sprites: pygame.sprite.Group, bounce_c: float = 0.8):
        super().__init__(other_sprites)
        self.rect = Ball.image.get_rect()
        pygame.transform.scale(dispy.display, (radius, radius))

        self.display = display
        self.x, self.y = cords
        self.rad = radius
        self.x_vel = x_velocity
        self.y_vel = y_velocity
        self.bounce_c = bounce_c
        self.spawn_check()

        self.gravy_objects = grav_objects

    def draw(self):
        pygame.draw.circle(self.display.display, self.colour, (self.x, self.y), self.rad)

    def spawn_check(self):
        status = self.check_borders(self.x, self.y)
        if status == 1:
            self.y = self.display.size[1] - self.rad - 1
            self.bounce()
        elif status == 2:
            self.x = self.rad + 1
            self.bounce_wall()
        elif status == 3:
            self.y = self.rad + 1
            self.bounce()
        elif status == 4:
            self.x = self.display.size[0] - self.rad - 1
            self.bounce_wall()

    def render(self):
        if self.x_vel != 0 or self.y_vel != 0:
            self.velocity_air_friction()
            self.change_cords()
            self.clear()
        self.be_gavitated()
        self.friction()
        self.draw()

    def update(self, *args, **kwargs):
        if self.x_vel != 0 or self.y_vel != 0:
            self.velocity_air_friction()
            self.change_cords()
            self.clear()
        self.be_gavitated()
        self.friction()

        self.rect.x = self.x - self.rad
        self.rect.y = self.y - self.rad

    def bounce(self):
        self.y_vel = -(self.y_vel * self.bounce_c - self.y_vel * self.display.friction_c)

    def bounce_wall(self):
        self.x_vel = -(self.x_vel * self.bounce_c - self.x_vel * self.display.friction_c)

    def check_borders(self, x, y):
        if x - self.rad <= 0:
            return 2
        elif x + self.rad >= self.display.size[0]:
            return 4
        elif y + self.rad >= self.display.size[1]:
            return 1
        elif y - self.rad <= 0:
            return 3

    def change_cords(self):
        new_x = self.x + self.x_vel / self.display.fps
        new_y = self.y + self.y_vel / self.display.fps
        status = self.check_borders(new_x, new_y)
        if status:
            if status % 2 == 0:
                self.bounce_wall()
            else:
                self.bounce()
        else:
            self.x = new_x
            self.y = new_y
        # print('I calculated my points: ', self.x_vel, self.y_vel, id(self))

    def be_sucked_to_a_point(self, obj, distance):
        self.x_vel += (obj.power / distance) * (1 if self.x < obj.x else -1)
        self.y_vel += (obj.power / distance) * (1 if self.y < obj.y else -1)

    def gravy_point_collision(self, obj):
        if isinstance(obj, BlackHole):
            obj.grow(self.rad)
            self.kill()

    def be_gavitated(self):
        for obj in self.gravy_objects:
            if isinstance(obj, Gravitron):
                if obj.gravity:
                    distance = (abs(self.y - obj.y)**2 + abs(self.x - obj.x)**2)**0.5
                    if distance > self.rad + obj.rad:
                        self.be_sucked_to_a_point(obj, distance)
                    else:
                        self.gravy_point_collision(obj)
        if self.display.gravity_c != 0:
            self.gravity_on_direction()

    def friction(self):
        if self.y + self.rad >= self.display.size[1] - 1 or self.y - self.rad <= 1:
            self.x_vel -= self.x_vel * self.display.friction_c
        if self.x - self.rad <= 1 or self.x + self.rad >= self.display.size[0] - 1:
            self.y_vel -= self.y_vel * self.display.friction_c

    def gravity_on_direction(self):
        if self.y + self.rad < self.display.size[1] and self.display.gravity_direction == 1:
            self.y_vel += self.display.gravity_c
        if self.y - self.rad > 0 and self.display.gravity_direction == 3:
            self.y_vel -= self.display.gravity_c
        if self.x - self.rad > 0 and self.display.gravity_direction == 2:
            self.x_vel -= self.display.gravity_c
        if self.x + self.rad < self.display.size[0] and self.display.gravity_direction == 4:
            self.x_vel += self.display.gravity_c

    def clear(self):
        if abs(round(self.x_vel / self.display.fps, 3)) < 0.05:
            self.x_vel = 0
        if abs(round(self.y_vel / self.display.fps, 3)) < 0.05:
            self.y_vel = 0

    def velocity_air_friction(self):
        self.x_vel -= round(self.x_vel * (self.display.air_loss / self.display.fps), 3)
        self.y_vel -= round(self.y_vel * (self.display.air_loss / self.display.fps), 3)

    def __str__(self):
        return str(id(self))

    def __repr__(self):
        return self.__str__()
