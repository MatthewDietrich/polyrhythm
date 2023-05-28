import sys

import pygame
import pygame.locals


class App:
    def __init__(self, config) -> None:
        pygame.init()
        self.config = config
        self.clock = pygame.time.Clock()
        self.start_time = self.clock.get_time()
        self.prev_draw_time = self.start_time

        self.window_size = config['window']['size']
        self.display_surf = pygame.display.set_mode(
            self.window_size,
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.base_duration = self.config['rhythm']['duration']
        self.base_velocity = self.window_size[0] / self.base_duration
        self.ball_radius = config['window']['ball_radius']
        self.ball_margin = config['window']['ball_margin']
        self.ball_positions = [0 for _ in self.config['rhythm']['notes']]
        self.ball_directions = [1 for _ in self.config['rhythm']['notes']]
        self.note_frequencies = [i for i in self.config['rhythm']['notes']]

    def _exit(self):
        print('Exiting')
        pygame.quit()
        sys.exit(0)

    def _draw(self):
        dt = self.clock.get_time()
        self.display_surf.fill(self.config['window']['background_color'])

        for i, x in enumerate(self.ball_positions):
            vel = self.base_velocity * (i + 1)
            if x / vel >= self.base_duration / (i + 1):
                self.ball_directions[i] = -self.ball_directions[i]
            x += 0.005 * vel * dt * self.ball_directions[i]
            y = (i + 1) * (2*self.ball_radius + self.ball_margin)
            pygame.draw.circle(
                self.display_surf,
                self.config['window']['ball_color'],
                (x, y),
                self.ball_radius
            )
            self.ball_positions[i] = x

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
