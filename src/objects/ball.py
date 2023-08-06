import pygame

from src.helpers import config
from src.helpers import utils


class Ball:
    def __init__(self, radius, position, direction, note) -> None:
        self.radius = radius
        self.position = position
        self.direction = direction
        self.color = tuple(config.BALL["color"])
        self.highlight_color = tuple(config.BALL["highlight_color"])
        self.note = note
        self.draw_color = self.color
        self.highlighted = False

    def start_highlight(self):
        self.highlighted = True
        self.draw_color = self.highlight_color

    def next_highlight(self):
        if self.highlighted:
            self.draw_color = utils.converge_color(
                self.draw_color, self.color, config.BALL["highlight_frames"]
            )
        if self.draw_color == self.color:
            self.highlighted = False

    def play_note(self):
        pygame.mixer.Sound.play(self.note)

    def draw(self, display_surf):
        pygame.draw.circle(display_surf, self.draw_color, self.position, self.radius)
