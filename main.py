from synthetic import *
from oxfordAffine import *
# from uav import *
# from airsim import *
# from drone import *
# from display import *

a = 100
b = 100
drawing = False
save = True
reconstruct = False
mobile = "_mobile2" # ""

execute_scenario_rotation (a, b, drawing, save, mobile)
execute_scenario_scale    (a, b, drawing, save, mobile)
execute_scenario_intensity(a, b, drawing, save, mobile)
executeScenarios          ("graf",   a, b, drawing, save, mobile)
executeScenarios          ("leuven", a, b, drawing, save, mobile)
executeScenarios          ("bark",   a, b, drawing, save, mobile)
executeScenarios          ("boat",   a, b, drawing, save, mobile)
executeScenarios          ("bikes",  a, b, drawing, save, mobile)
executeScenarios          ("trees",  a, b, drawing, save, mobile)
executeScenarios          ("wall",   a, b, drawing, save, mobile)
executeScenarios          ("ubc",    a, b, drawing, save, mobile)
# executeUAVScenarios       ("uav",    a, b, drawing, save, mobile)
# executeAirSimScenarios    ("airsim", a, b, drawing, save, mobile)
# executeDroneScenarios     ("drone",  a, b, drawing, save, mobile, reconstruct)

# syntheticAll4()
# synthetic4()
# single("synthetic")
# timing("synthetic")
# timing("synthetic", "_mobile")
# efficiency("synthetic")
# heatmap("synthetic")
# correlationHeatmap("synthetic")
# violinPlot("synthetic")

# oxfordAll9()
# oxford9()
# single("oxford")
# timing("oxford")
# timing("oxford", "_mobile")
# efficiency("oxford")
# heatmap("oxford")
# correlationHeatmap("oxford")
# violinPlot("oxford")

# singleAll("drone")
# single("drone")
# timing("drone")
# efficiency("drone")
# heatmap("drone")
# correlationHeatmap("drone")
# violinPlot("drone")

# singleAll("uav")
# single("uav")
# timing("uav")
# efficiency("uav")
# heatmap("uav")
# correlationHeatmap("uav")
# violinPlot("uav")

# singleAll("airsim")
# single("airsim")
# timing("airsim")
# efficiency("airsim")
# heatmap("airsim")
# correlationHeatmap("airsim")
# violinPlot("airsim")
