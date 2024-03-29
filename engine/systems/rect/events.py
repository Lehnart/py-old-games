import pygame

from engine.esper import Event


class HasMovedEvent(Event):

    def __init__(self, ent: int, previous_r: pygame.Rect, r: pygame.Rect):
        super().__init__()
        self.ent = ent
        self.previous_r = previous_r
        self.r = r


class SetPositionEvent(Event):

    def __init__(self, ent: int, x: float, y: float):
        super().__init__()
        self.ent = ent
        self.x = x
        self.y = y
