from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


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


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    "height": 20,
    "width": 20,
    "initial_sheep": 100,
    "initial_wolves": 10,
    "sheep_reproduce": 0.2,
    "wolf_reproduce": 0.03,
    "wolf_gain_from_food": 5,
    "grass": False,
    "grass_regrowth_time": 15,
    "sheep_gain_from_food": 20,
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
