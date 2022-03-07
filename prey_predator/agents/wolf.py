import random
from prey_predator.agents.random_walk import RandomWalker
import prey_predator.agents as agents


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.life_duration = 0

    def step(self):

        self.walk()
        self.energy -= 1
        self.eat_sheep()
        self.reproduce()
        if self.energy <= 0 or self.life_duration > self.model.wolf_lifespan:
            self.kill()
        self.life_duration += 1

    def walk(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        random.shuffle(next_moves)
        for move in next_moves:
            for entity in self.model.grid.get_cell_list_contents([move]):
                if type(entity) is agents.Sheep:
                    self.model.grid.move_agent(self, move)
                    return

        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def eat_sheep(self):
        for entity in self.model.grid.get_cell_list_contents([self.pos]):
            if type(entity) is agents.Sheep and self.energy < self.model.wolf_max_energy - self.model.wolf_gain_from_food:
                entity.kill()
                self.energy += self.model.wolf_gain_from_food
                continue

    def reproduce(self):
        if random.random() <= self.model.wolf_reproduce:
            baby = Wolf(self.model.current_id, self.pos, self.model, True, energy=0)
            self.model.schedule.add(baby)
            self.model.grid.place_agent(baby, self.pos)
            self.model.current_id += 1

    def kill(self):
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
