from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep

import random
import numpy as np

seed = 2022
random.seed(seed)
np.random.seed(seed)


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        # if agent.is_dead:
        #     return
        portrayal["Shape"] = "circle"
        portrayal["r"] = .5
        portrayal["Filled"] = True
        
        portrayal["Color"] = "white"
        portrayal["Layer"] = 2

    elif type(agent) is Wolf:
        # if agent.is_dead:
        #     return
        portrayal["Shape"] = "circle"
        portrayal["r"] = .8
        
        portrayal["Color"] = "red"
        portrayal["Filled"] = True
        portrayal["Layer"] = 1

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Filled"] = True
        portrayal["Layer"] = 0
        
        if agent.fully_grown:
            portrayal["Color"] = "#567d46"
        else:
            portrayal["Color"] = "#88FF88"
            
    return portrayal


model_params = {
    # Initial parameters
    "initial_sheep": UserSettableParameter("slider", "Initial number of sheep", 25, 0, 100),
    "initial_wolves": UserSettableParameter("slider", "Initial number of wolves", 3, 0, 25),
    # Reproduction
    "sheep_reproduce": UserSettableParameter("slider", "Probability of sheep reproduction", 0.1, 0, 1, step=5e-3),
    "wolf_reproduce": UserSettableParameter("slider", "Probability of wolf reproduction", 0.1, 0, 1, step=5e-3),
    # Eating
    "sheep_gain_from_food": UserSettableParameter("slider", "Sheep gain from food", 6, 0, 50),
    "wolf_gain_from_food": UserSettableParameter("slider", "Wolf gain from food", 10, 0, 50),
    "sheep_max_energy": UserSettableParameter("slider", "Sheep max energy", 75, 30, 100, step=5),
    "wolf_max_energy": UserSettableParameter("slider", "Wolf initial energy", 100, 30, 100, step=5),
    "grass_regrowth_time": UserSettableParameter("slider", "Grass initial energy", 30, 0, 50),
    "print_every": UserSettableParameter("slider", "Print every", 5, 0, 50)
}

canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#FF0000"}, {"Label": "Sheep", "Color": "#666666"}],
    canvas_height=400,
    canvas_width=1000
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
