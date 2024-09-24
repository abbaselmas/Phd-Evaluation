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
execute_scenario_intensity  (a, b, drawing, save)
execute_scenario_scale      (a, b, drawing, save)
execute_scenario_rotation   (a, b, drawing, save)
synthetic                   ()
syntheticMulti              ('Precision-Recall', 13, 12)
syntheticMulti              ('Inliers-Matches', 9, 10)
synthetic_timing            ()
synthetic_timing2           ()

## Oxford ##
executeScenarios("graf",   a, b, drawing, save)
executeScenarios("leuven", a, b, drawing, save)
executeScenarios("bark",   a, b, drawing, save)
executeScenarios("boat",   a, b, drawing, save)
executeScenarios("bikes",  a, b, drawing, save)
executeScenarios("trees",  a, b, drawing, save)
executeScenarios("wall",   a, b, drawing, save)
executeScenarios("ubc",    a, b, drawing, save)
oxford          ()
oxfordMulti     ('Precision-Recall', 13, 12)
oxfordMulti     ('Inliers-Matches', 9, 10)
oxford_timing   ()
oxford_timing2  ()

## Drone ##
executeDroneScenarios   ("drone", a, b, drawing, save)
single                  ('drone')
singleMulti             ('drone', 'Precision-Recall', 13, 12)
singleMulti             ('drone', 'Inliers-Matches',   9, 10)
single_timing           ('drone')
single_timing2          ('drone')

## UAV ##
executeUAVScenarios ("uav",   a, b, drawing, save)
single              ('uav')
singleMulti         ('uav', 'Precision-Recall', 13, 12)
singleMulti         ('uav', 'Inliers-Matches',   9, 10)
single_timing       ('uav')
single_timing2      ('uav')