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

execute_scenario_rotation (a, b, drawing, save, mobile)
execute_scenario_scale    (a, b, drawing, save, mobile)
execute_scenario_intensity(a, b, drawing, save, mobile)
synthetic                 ()
syntheticMulti            ("Precision-Recall", 13, 12)
syntheticMulti            ("Inliers-Matches",   9, 10)
synthetic_timing          ()
synthetic_timing2         ()
synthetic_timing_mobile   ()

executeScenarios          ("graf",   a, b, drawing, save, mobile)
executeScenarios          ("leuven", a, b, drawing, save, mobile)
executeScenarios          ("bark",   a, b, drawing, save, mobile)
executeScenarios          ("boat",   a, b, drawing, save, mobile)
executeScenarios          ("bikes",  a, b, drawing, save, mobile)
executeScenarios          ("trees",  a, b, drawing, save, mobile)
executeScenarios          ("wall",   a, b, drawing, save, mobile)
executeScenarios          ("ubc",    a, b, drawing, save, mobile)
oxford                    ()
oxfordMulti               ("Precision-Recall", 13, 12)
oxfordMulti               ("Inliers-Matches",   9, 10)
oxford_timing             ()
oxford_timing2            ()
oxford_timing_mobile      ()

executeDroneScenarios     ("drone",  a, b, drawing, save, reconstruct)
single                    ("drone")
singleMulti               ("drone", "Precision-Recall", 13, 12)
singleMulti               ("drone", "Inliers-Matches",   9, 10)
single_timing             ("drone")
single_timing2            ("drone")
rep_err                   ("drone")

executeUAVScenarios       ("uav",    a, b, drawing, save)
single                    ("uav")
singleMulti               ("uav", "Precision-Recall", 13, 12)
singleMulti               ("uav", "Inliers-Matches",   9, 10)
single_timing             ("uav")
single_timing2            ("uav")

executeAirSimScenarios    ("airsim", a, b, drawing, save)
single                    ("airsim")
singleMulti               ("airsim", "Precision-Recall", 13, 12)
singleMulti               ("airsim", "Inliers-Matches",   9, 10)
single_timing             ("airsim")
single_timing2            ("airsim")