from Objects import Ball, screen, dispy, fps
from Gravitron import BlackHole
import pygame


if __name__ == '__main__':
    godmod = False
    running = True

    clock = pygame.time.Clock()

    gravipopa = []
    sprites = pygame.sprite.Group()

    throw_power = 3
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F8]:
                    godmod = not godmod

            if godmod:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gravipopa.append(BlackHole(pygame.mouse.get_pos(), 6000, 15, dispy))
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_DELETE]:
                        sprites = pygame.sprite.Group()
                        gravipopa = []
                    elif keys[pygame.K_i]:
                        dispy.gravity_direction = 3
                    elif keys[pygame.K_j]:
                        dispy.gravity_direction = 2
                    elif keys[pygame.K_k]:
                        dispy.gravity_direction = 1
                    elif keys[pygame.K_l]:
                        dispy.gravity_direction = 4
                    elif keys[pygame.K_RIGHT]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, fps * throw_power, 0, gravipopa, sprites)
                    elif keys[pygame.K_LEFT]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, -fps * throw_power, 0, gravipopa, sprites)
                    elif keys[pygame.K_UP]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, 0, -fps * throw_power, gravipopa, sprites)
                    elif keys[pygame.K_DOWN]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, 0, fps * throw_power, gravipopa, sprites)

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

        sprites.draw(dispy.display)
        sprites.update()
        for gravipipa in gravipopa:
            gravipipa.render()

        pygame.display.flip()
        clock.tick(fps)
