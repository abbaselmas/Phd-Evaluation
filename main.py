from synthetic import *
from oxfordAffine import *
from drone import *
from uav import *
from display import *

a = 100
b = 100
drawing = False
save = True

## Synthetic ##
# execute_scenario_intensity(a, b, drawing, save)
# execute_scenario_scale    (a, b, drawing, save)
# execute_scenario_rotation (a, b, drawing, save)
synthetic()
syntheticMulti()
syntheticMulti('Inliers-Matches', 9, 10)
synthetic_timing()
synthetic_timing2()

## Oxford ##
# executeScenarios("graf",   a, b, drawing, save)
# executeScenarios("leuven", a, b, drawing, save)
# executeScenarios("bark",   a, b, drawing, save)
# executeScenarios("boat",   a, b, drawing, save)
# executeScenarios("bikes",  a, b, drawing, save)
# executeScenarios("trees",  a, b, drawing, save)
# executeScenarios("wall",   a, b, drawing, save)
# executeScenarios("ubc",    a, b, drawing, save)
oxford()
oxfordMulti()
oxfordMulti('Inliers-Matches', 9, 10)
oxford_timing()
oxford_timing2()

## Drone ##
# executeDroneScenarios("drone", a, b, drawing, save)
drone()
droneMulti()
droneMulti('Inliers-Matches', 9, 10)
drone_timing()
timing2('drone')

# executeUAVScenarios  ("uav",   a, b, drawing, save)
uav()
uavMulti()
uavMulti('Inliers-Matches', 9, 10)
uav_timing()
timing2('uav')