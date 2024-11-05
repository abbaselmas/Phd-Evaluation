import cv2
import numpy as np
import time, os
from define import *

def executeScenarios(folder, a=100, b=100, drawing=False, save=True, mobile=""):
    print(time.ctime() + f" {folder} started")
    print(f"Folder: {folder}")
    img = [cv2.imread(f"./oxfordAffine/{folder}/img{i}.jpg") for i in range(1, 7)]
    Rate      = np.load(f"./arrays/Rate_{folder}{mobile}.npy")      if os.path.exists(f"./arrays/Rate_{folder}{mobile}.npy")      else np.full((len(img)-1, 2, len(Normalization), len(Detectors), len(Descriptors), 16), np.nan)
    Exec_time = np.load(f"./arrays/Exec_time_{folder}{mobile}.npy") if os.path.exists(f"./arrays/Exec_time_{folder}{mobile}.npy") else np.full((len(img)-1, 2, len(Normalization), len(Detectors), len(Descriptors), 8), np.nan)
    keypoints_cache   = np.empty((len(img), len(Detectors), 2), dtype=object)
    descriptors_cache = np.empty((len(img), len(Detectors), len(Descriptors), 2), dtype=object)
    for k in range(len(img)-1):
        if drawing:
            if k != 3:
                continue
        for i in range(len(Detectors)):
            if (i == a or a == 100):
                method_dtect = Detectors[i]
                if keypoints_cache[0, i, 0] is None:
                    keypoints1 = method_dtect.detect(img[0], None)
                    keypoints_cache[0, i, 0] = keypoints1
                else:
                    keypoints1 = keypoints_cache[0, i, 0]
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
                                    if descriptors_cache[0, i, j, 0] is None:
                                        _, descriptors1 = method_dscrpt.compute(img[0], keypoints1)
                                        descriptors_cache[0, i, j, 0] = descriptors1
                                    else:
                                        descriptors1 = descriptors_cache[0, i, j, 0]
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
                                if drawing:
                                    img_matches = draw_matches(img[0], keypoints1, img[k+1], keypoints2, matches, inliers, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
                                    filename = f"./draws/{folder}/{k}_{method_dtect.getDefaultName().split('.')[-1]}_{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[m]}.png"
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
    print(time.ctime() + f" {folder} finished")