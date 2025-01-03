from synthetic import *
from oxfordAffine import *
from drone import *
from uav import *
from display import *
from airsim import *

a = 7
b = 0
drawing = False
save = False
reconstruct = True
mobile = "" # "_mobile"

# execute_scenario_scale        (          a, b, drawing, save)
# execute_scenario_intensity    (          a, b, drawing, save)
# execute_scenario_rotation     (          a, b, drawing, save)
# executeScenarios              ("graf",   a, b, drawing, save)
# executeScenarios              ("leuven", a, b, drawing, save)
# executeScenarios              ("bark",   a, b, drawing, save)
# executeScenarios              ("boat",   a, b, drawing, save)
# executeScenarios              ("bikes",  a, b, drawing, save)
# executeScenarios              ("trees",  a, b, drawing, save)
# executeScenarios              ("wall",   a, b, drawing, save)
# executeScenarios              ("ubc",    a, b, drawing, save)
# executeDroneScenarios         ("drone",  a, b, drawing, save, reconstruct)
# executeUAVScenarios           ("uav",    a, b, drawing, save)
# executeAirSimScenarios        ("airsim", a, b, drawing, save, reconstruct)

# synthetic           ()
# syntheticMulti      ("Precision-Recall", 13, 12)
# syntheticMulti      ("Inliers-Matches",   9, 10)
# synthetic_timing    ()
# synthetic_timing2   ()
# oxford              ()
# oxfordMulti         ("Precision-Recall", 13, 12)
# oxfordMulti         ("Inliers-Matches",   9, 10)
# oxford_timing       ()
# oxford_timing2      ()
# single              ("drone")
# singleMulti         ("drone", "Precision-Recall", 13, 12)
# singleMulti         ("drone", "Inliers-Matches",   9, 10)
# single_timing       ("drone")
# single_timing2      ("drone")
# single              ("uav")
# singleMulti         ("uav", "Precision-Recall", 13, 12)
# singleMulti         ("uav", "Inliers-Matches",   9, 10)
# single_timing       ("uav")
# single_timing2      ("uav")
# single              ("airsim")
# singleMulti         ("airsim", "Precision-Recall", 13, 12)
# singleMulti         ("airsim", "Inliers-Matches",   9, 10)
# single_timing       ("airsim")
# single_timing2      ("airsim")

# rep_err("drone")
# rep_err("airsim") #TODO: airsim should run with reconstruct true to fill Rate 11 with reprojetion error

# synthetic_timing_mobile()
# oxford_timing_mobile()

