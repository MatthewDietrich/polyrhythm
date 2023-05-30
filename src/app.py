import os
import sys

import numpy as np
import pygame
import pygame.locals
import yaml


with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)
WINDOW_CONFIG = CONFIG['window']
BALL_CONFIG = CONFIG['ball']
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
        self.color = tuple(BALL_CONFIG['color'])
        self.highlight_color = tuple(BALL_CONFIG['highlight_color'])
        self.note_frequency = note_frequency
        samples = np.arange(
            RHYTHM_CONFIG['note_duration'] * note_frequency
        )
        signal = np.sin(2 * np.pi * note_frequency * samples)
        signal *= 32767 # Magic number?
        signal = np.int8(signal)
        self.note = pygame.sndarray.make_sound(
            np.repeat(
                signal.reshape(len(signal), 1),
                2,
                axis=1
            )
        )
        self.draw_color = self.color
        self.highlighted = False

    def start_highlight(self):
        self.highlighted = True
        self.draw_color = self.highlight_color
    
    def next_highlight(self):
        if self.highlighted:
            self.draw_color = converge_color(
                self.draw_color,
                self.color,
                BALL_CONFIG['highlight_frames']
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
        borderless_flag = 0
        if WINDOW_CONFIG['borderless']:
            borderless_flag = pygame.NOFRAME
            os.environ['SDL_VIDEO_WINDOW_POS'] = '0.0'

        self.clock = pygame.time.Clock()
        self.start_time = self.clock.get_time()
        self.prev_draw_time = self.start_time

        self.window_size = WINDOW_CONFIG['size']
        self.background_color = WINDOW_CONFIG['background_color']
        self.display_surf = pygame.display.set_mode(
            self.window_size,
            pygame.HWSURFACE | pygame.DOUBLEBUF | borderless_flag
        )
        self.base_duration = RHYTHM_CONFIG['rhythm_duration'] * 1000
        self.base_velocity = self.window_size[0] / self.base_duration
        self.ball_radius = BALL_CONFIG['radius']
        self.ball_margin = BALL_CONFIG['margin']

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
            ball.next_highlight()
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
