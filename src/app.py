import os
import sys

import pygame
import pygame.locals
import yaml

from .utils import change_frequency, converge_color


with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)
WINDOW_CONFIG = CONFIG['window']
BALL_CONFIG = CONFIG['ball']
RHYTHM_CONFIG = CONFIG['rhythm']
MIXER_CONFIG = CONFIG['mixer']


pygame.init()
pygame.mixer.init(
    frequency=MIXER_CONFIG['frequency'],
    size=MIXER_CONFIG['size'],
    channels=MIXER_CONFIG['channels']
)

BASE_SOUND_ARRAY = pygame.sndarray.array(
    pygame.mixer.Sound(file=RHYTHM_CONFIG['base_sound'])
)


class Ball:
    def __init__(self, position, direction, note_frequency) -> None:
        self.position = position
        self.direction = direction
        self.color = tuple(BALL_CONFIG['color'])
        self.highlight_color = tuple(BALL_CONFIG['highlight_color'])
        self.note_frequency = note_frequency
        self.note = pygame.sndarray.make_sound(
            change_frequency(
                BASE_SOUND_ARRAY,
                MIXER_CONFIG['frequency'],
                note_frequency / RHYTHM_CONFIG['base_frequency']
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
        pygame.mixer.quit()
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
