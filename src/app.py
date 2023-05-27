import sys

import pygame
import pygame.locals


class App:
    def __init__(self, config) -> None:
        pygame.init()
        self.config = config
        self.clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode(
            (config['window']['width'], config['window']['height']),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

    def _exit(self):
        print('Exiting')
        pygame.quit()
        sys.exit(0)

    def _draw(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self._draw()
            pygame.display.flip()
        self._exit()
