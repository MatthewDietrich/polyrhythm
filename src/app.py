import os
import sys

import numpy as np
import pygame
import pygame.locals
import yaml


with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)
WINDOW_CONFIG = CONFIG['window']
RHYTHM_CONFIG = CONFIG['rhythm']


def converge(a, b, step):
    if a > b:
        if b == 0:
            b = a - 1
        return int(max(0, a - b/step))
    elif a < b:
        if b == 0:
            b = a + 1
        return int(min(255, a + b/step))
    return a


def converge_color(a, b, step):
    return tuple(
        converge(a[i], b[i], step)
        for i in range(len(a))
    )


class Ball:
    def __init__(self, position, direction, note_frequency) -> None:
        self.position = position
        self.direction = direction
        self.color = tuple(WINDOW_CONFIG['ball_color'])
        self.highlight_color = tuple(WINDOW_CONFIG['ball_highlight_color'])
        self.note_frequency = note_frequency
        self.note = pygame.mixer.Sound(
            buffer=(np.arange(
                RHYTHM_CONFIG['note_duration'] * self.note_frequency
            ) / self.note_frequency)
        )

        self.draw_color = self.color
        self.highlighted = False

    def start_highlight(self):
        self.highlighted = True
        self.draw_color = self.highlight_color
    
    def next_highlight(self, dt):
        if self.highlighted:
            self.draw_color = converge_color(
                self.draw_color,
                self.color,
                WINDOW_CONFIG['ball_highlight_frames']
            )
        if self.draw_color == self.color:
            self.highlighted = False

    def play_note(self):
        pygame.mixer.Sound.play(self.note)


class App:
    def __init__(self) -> None:
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=1
        )
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0.0'

        self.clock = pygame.time.Clock()
        self.start_time = self.clock.get_time()
        self.prev_draw_time = self.start_time

        self.window_size = WINDOW_CONFIG['size']
        self.background_color = WINDOW_CONFIG['background_color']
        self.display_surf = pygame.display.set_mode(
            self.window_size,
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME
        )
        self.base_duration = RHYTHM_CONFIG['rhythm_duration'] * 1000
        self.base_velocity = self.window_size[0] / self.base_duration
        self.ball_radius = WINDOW_CONFIG['ball_radius']
        self.ball_margin = WINDOW_CONFIG['ball_margin']

        self.balls = [Ball(
            position=self.ball_radius,
            direction=1,
            note_frequency=freq
        ) for freq in RHYTHM_CONFIG['notes']]

        self.elapsed = 0

    def _exit(self):
        print('Exiting')
        pygame.quit()
        sys.exit(0)

    def _draw(self):
        dt = self.clock.get_time()
        self.elapsed += dt
        self.display_surf.fill(self.background_color)
        for i, ball in enumerate(self.balls):
            interval = (i + 1) * self.base_duration
            x = int((self.elapsed % interval) / interval * self.window_size[0])
            prev_direction = ball.direction
            ball.direction = 1
            if int(self.elapsed / interval) % 2:
                ball.direction = -1
                x = self.window_size[0] - x
            if prev_direction != ball.direction:
                ball.start_highlight()
                ball.play_note()
            ball.next_highlight(dt)
            y = (i + 1) * (2*self.ball_radius + self.ball_margin)

            pygame.draw.circle(
                self.display_surf,
                ball.draw_color,
                (x, y),
                self.ball_radius
            )
            ball.position = x

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
