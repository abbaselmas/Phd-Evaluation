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
synthetic('Inliers', 9)
synthetic('Recall', 12)
synthetic('Precision', 13)
synthetic('Repeatibility', 14)
synthetic('F1Score', 15)
syntheticPR()
syntheticPR('Inliers-Matches', 9, 10)
synthetic_timing()

## Oxford ##
# executeScenarios("graf",   a, b, drawing, save)
# executeScenarios("leuven", a, b, drawing, save)
# executeScenarios("bark",   a, b, drawing, save)
# executeScenarios("boat",   a, b, drawing, save)
# executeScenarios("bikes",  a, b, drawing, save)
# executeScenarios("trees",  a, b, drawing, save)
# executeScenarios("wall",   a, b, drawing, save)
# executeScenarios("ubc",    a, b, drawing, save)
oxford('Inliers', 9)
oxford('Recall', 12)
oxford('Precision', 13)
oxford('Repeatibility', 14)
oxford('F1Score', 15)
oxfordPR()
oxfordPR('Inliers-Matches', 9, 10)
oxford_timing()

## Drone ##
# executeDroneScenarios("drone", a, b, drawing, save)
drone('Inliers', 9)
drone('Recall', 12)
drone('Precision', 13)
drone('Repeatibility', 14)
drone('F1Score', 15)
dronePR()
dronePR('Inliers-Matches', 9, 10)
drone_timing()

# executeUAVScenarios  ("uav",   a, b, drawing, save)
uav('Inliers', 9)
uav('Recall', 12)
uav('Precision', 13)
uav('Repeatibility', 14)
uav('F1Score', 15)
uavPR()
uavPR('Inliers-Matches', 9, 10)
uav_timing()