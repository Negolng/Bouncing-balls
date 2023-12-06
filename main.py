import pygame
from Gravitron import Display, BlackHole, Ball, Gravitron

if __name__ == '__main__':
    pygame.init()
    screensize = (900, 900)
    screen = pygame.display.set_mode(screensize)
    running = True
    clock = pygame.time.Clock()
    fps = 120
    dispy = Display(screen, screensize, fps, 0.001, 9.802, 0.1, 1)
    popa = []
    gravipopa = []
    throw_power = 3
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gravipopa.append(BlackHole(pygame.mouse.get_pos(), 6000, 15, dispy))
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    popa = []
                    gravipopa = []
                elif keys[pygame.K_RIGHT]:
                    popa.append(Ball(dispy, pygame.mouse.get_pos(), 15, fps * throw_power, 0, popa, gravipopa))
                elif keys[pygame.K_LEFT]:
                    popa.append(Ball(dispy, pygame.mouse.get_pos(), 15, -fps * throw_power, 0, popa, gravipopa))
                elif keys[pygame.K_UP]:
                    popa.append(Ball(dispy, pygame.mouse.get_pos(), 15, 0, -fps * throw_power, popa, gravipopa))
                elif keys[pygame.K_DOWN]:
                    popa.append(Ball(dispy, pygame.mouse.get_pos(), 15, 0, fps * throw_power, popa, gravipopa))

                elif keys[pygame.K_1]:
                    throw_power = 1
                elif keys[pygame.K_2]:
                    throw_power = 2
                elif keys[pygame.K_3]:
                    throw_power = 3
                elif keys[pygame.K_4]:
                    throw_power = 4
                elif keys[pygame.K_5]:
                    throw_power = 5
                elif keys[pygame.K_6]:
                    throw_power = 6
                elif keys[pygame.K_7]:
                    throw_power = 7
                elif keys[pygame.K_8]:
                    throw_power = 8
                elif keys[pygame.K_9]:
                    throw_power = 9
                elif keys[pygame.K_0]:
                    throw_power = 0

                elif keys[pygame.K_w]:
                    dispy.gravity_direction = 3
                elif keys[pygame.K_a]:
                    dispy.gravity_direction = 2
                elif keys[pygame.K_s]:
                    dispy.gravity_direction = 1
                elif keys[pygame.K_d]:
                    dispy.gravity_direction = 4

        for pipa in popa:
            pipa.render()
        for gravipipa in gravipopa:
            gravipipa.render()
        pygame.display.flip()
        clock.tick(fps)
