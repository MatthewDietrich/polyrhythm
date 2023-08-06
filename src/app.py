import os
import sys

import pygame
import pygame.locals

from .helpers.config import WINDOW_CONFIG, BALL_CONFIG, RHYTHM_CONFIG, MIXER_CONFIG
from .helpers.utils import change_frequency
from .objects.ball import Ball


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init(
            frequency=MIXER_CONFIG["frequency"],
            size=MIXER_CONFIG["size"],
            channels=MIXER_CONFIG["channels"],
        )

        self.base_sndarray = pygame.sndarray.array(
            pygame.mixer.Sound(file=RHYTHM_CONFIG["base_sound"])
        )

        self.clock = pygame.time.Clock()
        self.start_time = self.clock.get_time()
        self.prev_draw_time = self.start_time

        self.window_size = WINDOW_CONFIG["size"]
        self.background_color = WINDOW_CONFIG["background_color"]
        borderless_flag = 0
        if WINDOW_CONFIG["borderless"]:
            borderless_flag = pygame.NOFRAME
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0.0"
        self.display_surf = pygame.display.set_mode(
            self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF | borderless_flag
        )

        self.base_duration = RHYTHM_CONFIG["duration"] * 1000
        self.ball_radius = BALL_CONFIG["radius"]
        self.ball_margin = BALL_CONFIG["margin"]

        self.balls = [
            Ball(
                radius=self.ball_radius,
                position=(0, 0),
                direction=1,
                note=pygame.sndarray.make_sound(
                    change_frequency(
                        self.base_sndarray,
                        MIXER_CONFIG["frequency"],
                        freq / RHYTHM_CONFIG["base_frequency"],
                    )
                ),
            )
            for freq in RHYTHM_CONFIG["notes"]
        ]

        self.rhythm_margin = (
            self.window_size[1]
            - len(self.balls) * (2 * self.ball_radius + self.ball_margin)
        ) / 2

        self.elapsed = 0

    def _exit(self):
        print("Exiting")
        pygame.mixer.quit()
        pygame.quit()
        sys.exit(0)

    def _draw(self):
        dt = self.clock.get_time()
        self.elapsed += dt
        self.display_surf.fill(self.background_color)
        for i, ball in enumerate(self.balls):
            interval = (i * 0.1 + 2) * self.base_duration
            x = int((self.elapsed % interval) / interval * self.window_size[0])
            y = (i + 1) * (2 * self.ball_radius + self.ball_margin) + self.rhythm_margin
            prev_direction = ball.direction
            ball.direction = 1

            if int(self.elapsed / interval) % 2:
                ball.direction = -1
                x = self.window_size[0] - x
            if prev_direction != ball.direction:
                ball.start_highlight()
                ball.play_note()
            ball.next_highlight()

            ball.position = (x, y)
            ball.draw(self.display_surf)

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
