from mesa import Agent


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
        self.countdown = int(not fully_grown) * self.model.grass_regrowth_time
        self.fully_grown = fully_grown

    def step(self):
        # ... to be completed
        if self.countdown > 0:
            self.countdown -= 1
        self.fully_grown = self.countdown == 0

    def get_eaten(self):
        self.countdown = self.model.grass_regrowth_time
        self.fully_grown = False
