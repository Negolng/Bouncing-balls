from random import randint
import pygame


def rand_col():
    return tuple((randint(0, 255), randint(0, 255), randint(0, 255)))


class Display:
    __slots__ = ['display', 'size', 'fps', 'air_loss', 'gravity_c', 'friction_c', 'gravity_direction']

    def __init__(self, display: pygame.display, size: tuple, frps: int, loss: float, gravitation: float,
                 friction: float, direction: int):
        self.display = display
        self.size = size
        self.fps = frps
        self.air_loss = loss
        self.gravity_c = gravitation
        self.friction_c = friction
        self.gravity_direction = direction


class Gravitron:
    __slots__ = ['x', 'y', 'power', 'rad', 'gravity', 'sucker', 'display']

    def __init__(self, cords: tuple, power: float, rad: float, display: Display):
        self.x, self.y = cords
        self.power = power
        self.gravity = True
        self.sucker = False
        self.display = display
        self.rad = rad

    def render(self):
        pygame.draw.circle(self.display.display, (0, 0, 0), (self.x, self.y), self.rad)


class BlackHole(Gravitron):
    def __init__(self, cords: tuple, power: float, rad: int, display: Display):
        super().__init__(cords, power, rad, display)
        self.sucker = True

    def render(self):
        pygame.draw.circle(self.display.display, (0, 0, 0), (self.x, self.y), self.rad)

    def grow(self, rad):
        self.rad += rad / 10
        self.power += rad / 5


class Ball:
    __slots__ = ['display', 'x', 'y', 'rad', 'x_vel', 'y_vel', 'colour', 'bounce_c', 'others', 'gravy_objects']

    def __init__(self, display: Display, cords: tuple, radius: int, x_velocity: int | float, y_velocity: int | float,
                 others: list, grav_objects: list, bounce_c=0.8, colour: tuple = None):
        self.display = display
        self.x, self.y = cords
        self.rad = radius
        self.x_vel = x_velocity
        self.y_vel = y_velocity
        self.bounce_c = bounce_c
        if colour:
            self.colour = colour
        else:
            self.colour = rand_col()
        self.spawn_check()
        self.others = others
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
            if self in self.others:
                del self.others[self.others.index(self)]

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

    def __hash__(self):
        return hash((self.x, self.y, self.x_vel, self.y_vel, self.rad, self.colour, self.bounce_c))
