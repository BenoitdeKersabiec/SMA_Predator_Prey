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
    # Initial parameters
    "initial_sheep": UserSettableParameter("slider", "Initial number of sheep", 25, 0, 100),
    "initial_wolves": UserSettableParameter("slider", "Initial number of wolves", 3, 0, 25),
    # Reproduction
    "sheep_reproduce": UserSettableParameter("slider", "Probability of sheep reproduction", 0.1, 0, 1, step=5e-3),
    "wolf_reproduce": UserSettableParameter("slider", "Probability of wolf reproduction", 0.1, 0, 1, step=5e-3),
    # Eating
    "sheep_gain_from_food": UserSettableParameter("slider", "Sheep gain from food", 20, 0, 50),
    "wolf_gain_from_food": UserSettableParameter("slider", "Wolf gain from food", 10, 0, 50),
    "sheep_max_energy": UserSettableParameter("slider", "Sheep max energy", 50, 30, 100, step=5),
    "wolf_max_energy": UserSettableParameter("slider", "Wolf max energy", 50, 30, 100, step=5),
    "sheep_lifespan": UserSettableParameter("slider", "Sheep lifespan", 200, 60, 250, step=5),
    "wolf_lifespan": UserSettableParameter("slider", "Wolf lifespan", 200, 60, 250, step=5),
    "grass_regrowth_time": UserSettableParameter("slider", "Grass regrowth time", 30, 0, 50),
}

canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves (x3)", "Color": "#FF0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
