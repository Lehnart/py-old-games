import random

import pygame

from engine.esper import World
from engine.systems.input.components import InputComponent
from engine.systems.input.processors import InputProcessor
from engine.systems.rect.components import RectComponent
from engine.systems.rect.processors import RectProcessor
from engine.systems.render.components import WindowComponent
from engine.systems.render.processors import RenderProcessor
from engine.systems.speed.events import MoveRectEvent
from engine.systems.sprite.components import SpriteComponent
from engine.systems.sprite.processors import SpriteProcessor
from engine.systems.sprite_string.components import StringSpriteComponent
from engine.systems.sprite_string.processors import StringSpriteProcessor
from py_autobots.config import WINDOW_SIZE, FRAME_RATE, HERO_RECT, HERO_SPRITE, TILE_SIZE, GRASS_SPRITE, TREE_SPRITE, \
    BRANCH_SPRITE, ROCK_SPRITE, WORKSHOP_RECT, WORKSHOP_SPRITE, TILE_COUNT, MENU_FONT
from py_autobots.systems.plan.events import CreatePlanEvent
from py_autobots.systems.plan.processors import PlanProcessor
from py_autobots.systems.plan_menu.components import PlanMenuComponent
from py_autobots.systems.plan_menu.events import NextPlanEvent, PreviousPlanEvent
from py_autobots.systems.plan_menu.processors import PlanMenuProcessor
from py_autobots.systems.plan_menu_item.components import PlanMenuItemComponent
from py_autobots.systems.plan_menu_item.processors import PlanMenuItemProcessor


def create_plan(w: World, e: int):
    r = w.component_for_entity(e, RectComponent)
    l = w.get_component(PlanMenuItemComponent)
    plan_name = None
    for e, c in l:
        if c.is_selected:
            plan_name = c.name

    if plan_name:
        w.publish(CreatePlanEvent(plan_name, r.x, r.y))


class PyAutobots(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        # Window entity
        window = WindowComponent(WINDOW_SIZE)
        self.create_entity(window)

        # hero entity
        rect = RectComponent(*HERO_RECT)
        sprite = SpriteComponent(HERO_RECT[0], HERO_RECT[1], HERO_SPRITE, 1)
        hero = self.create_entity(rect, sprite)

        self.add_component(
            hero,
            InputComponent(
                {
                    pygame.K_z: lambda w, e: w.publish(MoveRectEvent(e, 0, -TILE_SIZE)),
                    pygame.K_s: lambda w, e: w.publish(MoveRectEvent(e, 0, TILE_SIZE)),
                    pygame.K_q: lambda w, e: w.publish(MoveRectEvent(e, -TILE_SIZE, 0)),
                    pygame.K_d: lambda w, e: w.publish(MoveRectEvent(e, TILE_SIZE, 0)),
                    pygame.K_e: create_plan
                },
                is_repeat=False
            )
        )

        # PlanItem entity
        workshop = self.create_entity(
            PlanMenuItemComponent("Workshop"),
            StringSpriteComponent("Workshop", MENU_FONT, pygame.Color(255, 255, 255), (810, 24))
        )
        item1 = self.create_entity(
            PlanMenuItemComponent("Item1"),
            StringSpriteComponent("Item1", MENU_FONT, pygame.Color(255, 255, 255), (810, 72))
        )
        item2 = self.create_entity(
            PlanMenuItemComponent("Item2"),
            StringSpriteComponent("Item2", MENU_FONT, pygame.Color(255, 255, 255), (810, 120))
        )

        # PlanMenu entity
        menu = self.create_entity(
            PlanMenuComponent([workshop, item1, item2]),
            InputComponent(
                {
                    pygame.K_UP: lambda w, e: w.publish(PreviousPlanEvent(e)),
                    pygame.K_DOWN: lambda w, e: w.publish(NextPlanEvent(e)),
                },
                is_repeat=False
            )
        )

        # workshop entity
        rect = RectComponent(*WORKSHOP_RECT)
        sprite = SpriteComponent(WORKSHOP_RECT[0], WORKSHOP_RECT[1], WORKSHOP_SPRITE, 1)
        workshop = self.create_entity(rect, sprite)

        for i in range(0, TILE_COUNT):
            for j in range(0, TILE_COUNT):
                x = TILE_SIZE * i
                y = TILE_SIZE * j
                rect = RectComponent(x, y, TILE_SIZE, TILE_SIZE)
                sprite = SpriteComponent(x, y, GRASS_SPRITE)
                grass = self.create_entity(rect, sprite)

        for i in range(0, TILE_COUNT):
            for j in range(0, TILE_COUNT):
                x = TILE_SIZE * i
                y = TILE_SIZE * j

                rect = RectComponent(x, y, TILE_SIZE, TILE_SIZE)
                sprite = None
                if random.random() < 10. / 625.:
                    sprite = SpriteComponent(x, y, TREE_SPRITE)
                elif random.random() < 10. / 625.:
                    sprite = SpriteComponent(x, y, BRANCH_SPRITE)
                elif random.random() < 10. / 625.:
                    sprite = SpriteComponent(x, y, ROCK_SPRITE)

                ent = self.create_entity(rect, sprite, 1)

        self.add_processor(InputProcessor(), 20)
        self.add_processor(PlanMenuProcessor(), 19)
        self.add_processor(PlanMenuItemProcessor(), 19)
        self.add_processor(PlanProcessor(), 19)
        self.add_processor(StringSpriteProcessor(), 17)
        self.add_processor(SpriteProcessor(), 16)
        self.add_processor(RectProcessor(), 16)
        self.add_processor(RenderProcessor(FRAME_RATE), 9)

    def is_running(self) -> bool:
        return self._is_running


def run():
    game_world = PyAutobots()
    while game_world.is_running():
        game_world.process()


if __name__ == '__main__':
    run()
