from engine.esper import Processor
from engine.systems.sprite_string.events import SetStringEvent
from py_breakout.systems.life.components import LifeComponent
from py_breakout.systems.life.events import DecreaseLifeEvent, NewLifeValueEvent


class LifeProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        for event in self.world.receive(DecreaseLifeEvent):
            life_comps = self.world.get_component(LifeComponent)
            for ent, life_comp in life_comps:
                life_comp.life -= 1
                self.world.publish(SetStringEvent(ent, str(life_comp.life)))
                self.world.publish(NewLifeValueEvent(life_comp.life))
