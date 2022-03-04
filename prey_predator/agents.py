import random
from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=0):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """

        self.random_move()
        self.energy -= 1
        self.eat_grass()
        self.reproduce()
        if self.energy <= 0:
            self.kill()

    def eat_grass(self):
        for entity in self.model.grid.get_cell_list_contents([self.pos]):
            if type(entity) is GrassPatch:
                if entity.fully_grown:
                    entity.countdown = self.model.grass_regrowth_time
                    entity.fully_grown = False
                    self.energy += self.model.sheep_gain_from_food
                    continue

    def reproduce(self):
        if random.random() <= self.model.sheep_reproduce:
            baby = Sheep(self.model.current_id, self.pos, self.model, False, energy=0)
            self.model.schedule.add(baby)
            self.model.grid.place_agent(baby, self.pos)
            self.model.current_id += 1

    def kill(self):
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):

        self.random_move()
        self.energy -= 1
        self.eat_sheep()
        self.reproduce()
        if self.energy <= 0:
            self.kill()
    
    def eat_sheep(self):
        for entity in self.model.grid.get_cell_list_contents([self.pos]):
            if type(entity) is Sheep:
                entity.kill()
                self.energy += self.model.wolf_gain_from_food
                continue

    def reproduce(self):
        if random.random() <= self.model.wolf_reproduce:
            baby = Wolf(self.model.current_id, self.pos, self.model, False, energy=0)
            self.model.schedule.add(baby)
            self.model.grid.place_agent(baby, self.pos)
            self.model.current_id += 1

    def kill(self):
        if self.unique_id in self.model.schedule._agents:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)



class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.countdown = int(not fully_grown) * (model.grass_regrowth_time)
        self.fully_grown = fully_grown

    def step(self):
        # ... to be completed
        if self.countdown > 0:
            self.countdown -= 1
        self.fully_grown = self.countdown == 0
