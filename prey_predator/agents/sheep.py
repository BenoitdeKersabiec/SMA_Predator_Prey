import random
from prey_predator.agents.random_walk import RandomWalker
import prey_predator.agents as agents


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=0):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.life_duration = 0

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """

        self.walk()
        self.energy -= 1
        self.eat()
        self.reproduce()
        if self.energy <= 0 or self.life_duration > self.model.sheep_lifespan:
            self.kill()
        self.life_duration += 1

    def walk(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        # Avoid the woves
        wolves = []
        for position in next_moves:
            for entity in self.model.grid.get_cell_list_contents([position]):
                if type(entity) is agents.Wolf:
                    x, y = position
                    wolves.append((x, y))
                    wolves.append((x + 1, y))
                    wolves.append((x, y + 1))
                    wolves.append((x + 1, y + 1))

        life_moves = list(set(next_moves).difference(set(wolves)))
        if len(life_moves) > 0:
            next_moves = life_moves
        # Seek for grass
        random.shuffle(next_moves)
        for move in next_moves:
            for entity in self.model.grid.get_cell_list_contents([move]):
                if type(entity) is agents.GrassPatch:
                    self.model.grid.move_agent(self, move)
                    return

        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def eat(self):
        for entity in self.model.grid.get_cell_list_contents([self.pos]):
            if type(entity) is agents.GrassPatch:
                if entity.fully_grown and self.energy < self.model.sheep_max_energy - self.model.sheep_gain_from_food:
                    entity.get_eaten()
                    self.energy += self.model.sheep_gain_from_food
                    continue

    def reproduce(self):
        if random.random() <= self.model.sheep_reproduce:
            baby = Sheep(self.model.current_id, self.pos, self.model, True, energy=0)
            self.model.schedule.add(baby)
            self.model.grid.place_agent(baby, self.pos)
            self.model.current_id += 1

    def kill(self):
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)



