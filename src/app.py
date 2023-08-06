import os
import sys

import pygame
import pygame.locals

from src.helpers import config, utils
from src.objects import ball


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init(
            frequency=config.MIXER["frequency"],
            size=config.MIXER["size"],
            channels=config.MIXER["channels"],
        )

        self.base_sndarray = pygame.sndarray.array(
            pygame.mixer.Sound(file=config.RHYTHM["base_sound"])
        )

        self.clock = pygame.time.Clock()
        self.start_time = self.clock.get_time()
        self.prev_draw_time = self.start_time

        self.window_size = config.WINDOW["size"]
        self.background_color = config.WINDOW["background_color"]
        borderless_flag = 0
        if config.WINDOW["borderless"]:
            borderless_flag = pygame.NOFRAME
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0.0"
        self.display_surf = pygame.display.set_mode(
            self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF | borderless_flag
        )

        self.base_duration = config.RHYTHM["duration"] * 1000
        self.ball_radius = config.BALL["radius"]
        self.ball_margin = config.BALL["margin"]

        self.balls = [
            ball.Ball(
                radius=self.ball_radius,
                position=(0, 0),
                direction=1,
                note=pygame.sndarray.make_sound(
                    utils.change_frequency(
                        self.base_sndarray,
                        config.MIXER["frequency"],
                        freq / config.RHYTHM["base_frequency"],
                    )
                ),
            )
            for freq in config.RHYTHM["notes"]
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
