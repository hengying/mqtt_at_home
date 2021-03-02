import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from config import Config

from button_enum import ButtonType

from event import *

class DesktopWin():
    def __init__(self):
        self._config = Config()
        self._width = self._config.pygame_win_width
        self._height = self._config.pygame_win_height

        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height), pygame.NOFRAME)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def update(self, event_queue):
        while True:
            e = pygame.event.poll()
            if e.type == pygame.NOEVENT:
                break;

            if e.type == pygame.QUIT:
                event_queue.put_nowait(QuitEvent())
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    event_queue.put_nowait(QuitEvent())
                elif e.key == pygame.K_UP:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_UP))
                elif e.key == pygame.K_LEFT:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_LEFT))
                elif e.key == pygame.K_RIGHT:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_RIGHT))
                elif e.key == pygame.K_DOWN:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_DOWN))
                elif e.key == pygame.K_SPACE:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_PRESS))
                elif e.key == pygame.K_z:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.BUTTON_1))
                elif e.key == pygame.K_x:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.BUTTON_2))
                elif e.key == pygame.K_c:
                    event_queue.put_nowait(ButtonDownEvent(ButtonType.BUTTON_3))
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_UP))
                elif e.key == pygame.K_LEFT:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_LEFT))
                elif e.key == pygame.K_RIGHT:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_RIGHT))
                elif e.key == pygame.K_DOWN:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_DOWN))
                elif e.key == pygame.K_SPACE:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_PRESS))
                elif e.key == pygame.K_z:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.BUTTON_1))
                elif e.key == pygame.K_x:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.BUTTON_2))
                elif e.key == pygame.K_c:
                    event_queue.put_nowait(ButtonUpEvent(ButtonType.BUTTON_3))

    def display(self, image):
        rgb_image = image.convert('RGB')
        mode = rgb_image.mode
        size = rgb_image.size
        data = rgb_image.tobytes()

        pygame_image = pygame.image.fromstring(data, size, mode)

        self._screen.blit(pygame_image, (0, 0, size[0], size[1]))

        pygame.display.flip()
