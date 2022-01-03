import pygame

from engine.esper import World
from engine.systems.input.components import InputComponent
from engine.systems.input.processors import InputProcessor
from engine.systems.rect.components import RectComponent, RectLimitComponent
from engine.systems.rect.events import MoveEvent
from engine.systems.rect.processors import RectProcessor
from engine.systems.rectsprite.components import RectSpriteComponent
from engine.systems.rectsprite.processors import RectSpriteProcessor
from engine.systems.render.components import WindowComponent
from engine.systems.render.processors import RenderProcessor
from engine.systems.sprite.components import SpriteComponent

PADDLE_SPEED = 500


class PyPong(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        # Window entity
        window = WindowComponent((800, 840))
        self.create_entity(window)

        # left paddle entity
        rect = RectComponent(5, 400, 20, 80)
        rect_limit = RectLimitComponent(0, 800, 0, 840)
        rect_sprite = RectSpriteComponent(pygame.Rect(5, 400, 20, 80), pygame.Color("white"))
        paddle1 = self.create_entity(rect, rect_limit, rect_sprite)

        self.add_component(
            paddle1,
            InputComponent(
                {
                    pygame.K_UP: lambda w: w.publish(MoveEvent(paddle1, 0, -w.process_dt * PADDLE_SPEED)),
                    pygame.K_DOWN: lambda w: w.publish(MoveEvent(paddle1, 0, +w.process_dt * PADDLE_SPEED)),
                }
            )
        )

        # Right paddle entity
        rect = RectComponent(775, 400, 20, 80)
        rect_limit = RectLimitComponent(0, 800, 0, 840)
        rect_sprite = RectSpriteComponent(pygame.Rect(775, 400, 20, 80), pygame.Color("white"))
        paddle2 = self.create_entity(rect, rect_limit, rect_sprite)
        self.add_component(
            paddle2,
            InputComponent(
                {
                    pygame.K_i: lambda w: w.publish(MoveEvent(paddle2, 0, -w.process_dt * PADDLE_SPEED)),
                    pygame.K_k: lambda w: w.publish(MoveEvent(paddle2, 0, +w.process_dt * PADDLE_SPEED)),
                }
            )
        )

        # center line
        center_line_surf = pygame.Surface((5, 840))
        h_segment = 10
        y0 = 0
        while y0 + h_segment < 840:
            pygame.draw.rect(center_line_surf, (255, 255, 255), (0, y0, 5, h_segment))
            y0 += 2 * h_segment
        sprite = SpriteComponent(398,0, center_line_surf)
        center_line = self.create_entity(sprite)

        self.add_processor(RenderProcessor(), 1)
        self.add_processor(InputProcessor(), 2)
        self.add_processor(RectProcessor(), 3)
        self.add_processor(RectSpriteProcessor(), 4)

    def is_running(self) -> bool:
        return self._is_running


def run():
    game_world = PyPong()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    # import cProfile
    # cProfile.run('run()', sort="cumtime")
    run()
