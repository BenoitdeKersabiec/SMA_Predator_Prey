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

        self.walk()
        self.energy -= 1
        self.eat_grass()
        self.reproduce()
        if self.energy <= 0:
            self.kill()

    def walk(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        # Avoid the woves
        wolves = []
        for position in next_moves:
            for entity in self.model.grid.get_cell_list_contents([position]):
                if type(entity) is Wolf:
                    x, y = position
                    wolves.append((x, y))
                    wolves.append((x + 1, y))
                    wolves.append((x, y + 1))
                    wolves.append((x + 1, y + 1))

        next_moves = list(set(next_moves).difference(set(wolves)))
        # Seek for grass
        random.shuffle(next_moves)
        for move in next_moves:
            for entity in self.model.grid.get_cell_list_contents([move]):
                if type(entity) is GrassPatch:
                    self.model.grid.move_agent(self, move)
                    return

        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

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
            baby = Sheep(self.model.current_id, self.pos, self.model, True, energy=0)
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

        self.walk()
        self.energy -= 1
        self.eat_sheep()
        self.reproduce()
        if self.energy <= 0:
            self.kill()

    def walk(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        random.shuffle(next_moves)
        for move in next_moves:
            for entity in self.model.grid.get_cell_list_contents([move]):
                if type(entity) is Sheep:
                    self.model.grid.move_agent(self, move)
                    return

        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
    
    def eat_sheep(self):
        for entity in self.model.grid.get_cell_list_contents([self.pos]):
            if type(entity) is Sheep:
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
