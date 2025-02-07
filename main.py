from synthetic import *
from oxfordAffine import *
from drone import *
from uav import *
from display import *
from airsim import *

a = 100
b = 100
drawing = False
save = True
reconstruct = True
mobile = "" # "_mobile"

# execute_scenario_rotation (a, b, drawing, save, mobile)
# execute_scenario_scale    (a, b, drawing, save, mobile)
# execute_scenario_intensity(a, b, drawing, save, mobile)
# executeScenarios          ("graf",   a, b, drawing, save, mobile)
# executeScenarios          ("leuven", a, b, drawing, save, mobile)
# executeScenarios          ("bark",   a, b, drawing, save, mobile)
# executeScenarios          ("boat",   a, b, drawing, save, mobile)
# executeScenarios          ("bikes",  a, b, drawing, save, mobile)
# executeScenarios          ("trees",  a, b, drawing, save, mobile)
# executeScenarios          ("wall",   a, b, drawing, save, mobile)
# executeScenarios          ("ubc",    a, b, drawing, save, mobile)
# executeDroneScenarios     ("drone",  a, b, drawing, save, mobile, reconstruct)
# executeUAVScenarios       ("uav",    a, b, drawing, save, mobile)
# executeAirSimScenarios    ("airsim", a, b, drawing, save, mobile, reconstruct)

syntheticAll4()
synthetic4()
synthetic()
syntheticTiming()

oxfordAll9()
oxford9()
oxford()
oxfordTiming()

singleAll("drone")
singleTiming("drone")
single("drone")

singleAll("uav")
singleTiming("uav")
single("uav")

singleAll("airsim")
singleTiming("airsim")
single("airsim")