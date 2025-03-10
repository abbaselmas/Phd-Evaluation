import cv2
import numpy as np
import time, os
from define import *
from database import *

def executeAirSimScenarios(folder="airsim", a=100, b=100, drawing=False, save=True, mobile=""):
    print(time.ctime())
    print(f"Folder: {folder}")
    image_folder = "./Datasets/AirSimNH/Layer3/pitch-90_yaw0"
    img = []
    files = sorted(os.listdir(image_folder))
    for filename in files:
        img.append(cv2.imread(os.path.join(image_folder, filename)))
    Rate      = np.load(f"./arrays/Rate_{folder}{mobile}.npy")      if os.path.exists(f"./arrays/Rate_{folder}{mobile}.npy")      else np.full((len(img)-1, 2, len(Normalization), len(Detectors), len(Descriptors), 17), np.nan)
    Exec_time = np.load(f"./arrays/Exec_time_{folder}{mobile}.npy") if os.path.exists(f"./arrays/Exec_time_{folder}{mobile}.npy") else np.full((len(img)-1, 2, len(Normalization), len(Detectors), len(Descriptors), 9), np.nan)
    keypoints_cache   = np.empty((len(img), len(Detectors), 2), dtype=object)
    descriptors_cache = np.empty((len(img), len(Detectors), len(Descriptors), 2), dtype=object)
    for k in range(len(img)-1):
        if drawing and k != 2:
            continue
        for i in range(len(Detectors)):
            if (i == a or a == 100):
                method_dtect = Detectors[i]
                if keypoints_cache[k, i, 0] is None:
                    keypoints1 = method_dtect.detect(img[k], None)
                    keypoints_cache[k, i, 0] = keypoints1
                else:
                    keypoints1 = keypoints_cache[k, i, 0]
                if keypoints_cache[k+1, i, 1] is None:
                    start_time = time.perf_counter_ns()
                    keypoints2 = method_dtect.detect(img[k+1], None)
                    detect_time = time.perf_counter_ns() - start_time
                    keypoints_cache[k+1, i, 1] = keypoints2
                else:
                    keypoints2 = keypoints_cache[k+1, i, 1]
                for j in range(len(Descriptors)):
                    if j == b or b == 100:
                        method_dscrpt = Descriptors[j]
                        for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                            for m in range(2): # Matching Type 0: BruteForce 1: FlannBased
                                try:
                                    if descriptors_cache[k, i, j, 0] is None:
                                        _, descriptors1 = method_dscrpt.compute(img[k], keypoints1)
                                        descriptors_cache[k, i, j, 0] = descriptors1
                                    else:
                                        descriptors1 = descriptors_cache[k, i, j, 0]
                                    if descriptors_cache[k+1, i, j, 1] is None:
                                        start_time = time.perf_counter_ns()
                                        _, descriptors2 = method_dscrpt.compute(img[k+1], keypoints2)
                                        descript_time = time.perf_counter_ns() - start_time
                                        descriptors_cache[k+1, i, j, 1] = descriptors2
                                    else:
                                        descriptors2 = descriptors_cache[k+1, i, j, 1]
                                    start_time = time.perf_counter_ns()
                                    inliers, matches = evaluate_with_fundamentalMat_and_XSAC(m, keypoints1, keypoints2, descriptors1, descriptors2, Normalization[c3])
                                    Exec_time[k, m, c3, i, j, 2] = (time.perf_counter_ns() - start_time) / (10 ** 9)
                                    Rate, Exec_time = process_matches(Rate, Exec_time, k, m, c3, i, j, len(keypoints1), len(keypoints2), len(descriptors1), len(descriptors2), len(inliers), len(matches), detect_time, descript_time)
                                except:
                                    Exec_time[k, m, c3, i, j, :] = None
                                    Rate[k, m, c3, i, j, 5:16] = None
                                    continue
                                if drawing and Rate[k, m, c3, i, j, 9] > 500 and Rate[k, m, c3, i, j, 13] > 0.85 and Exec_time[k, m, c3, i, j, 7] < 0.5:
                                    img_matches = draw_matches(img[k], keypoints1, img[k+1], keypoints2, matches, inliers, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
                                    filename = f"./draws/{folder}/{k}_{i}{method_dtect.getDefaultName().split('.')[-1]}_{j}{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[m]}.png"
                                    cv2.imwrite(filename, img_matches)
                    else:
                        continue
            else:
                continue
    if save:
        np.save(f"./arrays/Rate_{folder}{mobile}.npy",      Rate)
        np.save(f"./arrays/Exec_time_{folder}{mobile}.npy", Exec_time)
        saveAverageCSV(Rate, Exec_time, folder, mobile)
        saveAllCSV(Rate, Exec_time, folder, mobile)
    print(time.ctime() + f" {folder} finished\n")