import pygame

from ..helpers.config import BALL_CONFIG
from ..helpers.utils import converge_color


class Ball:
    def __init__(self, radius, position, direction, note) -> None:
        self.radius = radius
        self.position = position
        self.direction = direction
        self.color = tuple(BALL_CONFIG["color"])
        self.highlight_color = tuple(BALL_CONFIG["highlight_color"])
        self.note = note
        self.draw_color = self.color
        self.highlighted = False

    def start_highlight(self):
        self.highlighted = True
        self.draw_color = self.highlight_color

    def next_highlight(self):
        if self.highlighted:
            self.draw_color = converge_color(
                self.draw_color, self.color, BALL_CONFIG["highlight_frames"]
            )
        if self.draw_color == self.color:
            self.highlighted = False

    def play_note(self):
        pygame.mixer.Sound.play(self.note)

    def draw(self, display_surf):
        pygame.draw.circle(display_surf, self.draw_color, self.position, self.radius)
