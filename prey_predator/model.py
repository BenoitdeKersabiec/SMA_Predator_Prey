"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves (x3)": lambda m: 3 * m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )
        self.current_id = 0


        # Create sheep:
        for sheep_id in range(initial_sheep):
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            sheep = Sheep(self.current_id, (x, y), self, True, energy=10)
            self.schedule.add(sheep)
            # Add the agent to a random grid cell
            self.grid.place_agent(sheep, (x, y))
            self.current_id += 1
            
        # Create wolves
        for wolf_id in range(initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            wolf = Wolf(self.current_id, (x, y), self, True, energy=50)
            self.schedule.add(wolf)
            # Add the agent to a random grid cell
            self.grid.place_agent(wolf, (x, y))
            self.current_id += 1
            
        # Create grass patches
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                grass = GrassPatch(self.current_id, (x, y), self, True, countdown=0)
                self.schedule.add(grass)
                # Add the agent to a random grid cell
                self.grid.place_agent(grass, (x, y))
                self.current_id += 1

    def step(self):
        self.schedule.step(by_breed=True)

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    def run_model(self, step_count=200):

        # ... to be completed
        pass

