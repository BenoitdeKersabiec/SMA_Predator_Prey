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


model_params = {
    "initial_sheep": UserSettableParameter("slider", "initial_sheep", 25, 0, 100),
    "initial_wolves": UserSettableParameter("slider", "initial_wolves", 3, 0, 25),
    "sheep_reproduce": UserSettableParameter("slider", "sheep_reproduce", 0.1, 0, 1, step=1e-3),
    "wolf_reproduce": UserSettableParameter("slider", "wolf_reproduce", 0.1, 0, 1, step=1e-3),
    "sheep_gain_from_food": UserSettableParameter("slider", "sheep_gain_from_food", 20, 0, 50),
    "wolf_gain_from_food": UserSettableParameter("slider", "wolf_gain_from_food", 10, 0, 50),
    "grass_regrowth_time": UserSettableParameter("slider", "grass_regrowth_time", 30, 0, 50),
}

canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves (x3)", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
