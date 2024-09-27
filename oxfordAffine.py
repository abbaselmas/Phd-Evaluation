import cv2
import numpy as np
import time, os
from define import *

def executeScenarios(folder, a=100, b=100, drawing=False, save=True):
    print(time.ctime())
    print(f"Folder: {folder}")
    img = [cv2.imread(f"./oxfordAffine/{folder}/img{i}.jpg") for i in range(1, 7)]
    Rate      = np.load(f"./arrays/Rate_{folder}.npy")      if os.path.exists(f"./arrays/Rate_{folder}.npy")      else np.full((len(img)-1, 2, len(Normalization), len(Detectors), len(Descriptors), 16), np.nan)
    Exec_time = np.load(f"./arrays/Exec_time_{folder}.npy") if os.path.exists(f"./arrays/Exec_time_{folder}.npy") else np.full((len(img)-1, 2, len(Normalization), len(Detectors), len(Descriptors), 8), np.nan)
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
                                Exec_time[k, m, c3, i, j, 0] = detect_time / (10 ** 9)
                                Rate[k, m, c3, i, j, 0] = k
                                Rate[k, m, c3, i, j, 1] = i
                                Rate[k, m, c3, i, j, 2] = j
                                Rate[k, m, c3, i, j, 3] = Normalization[c3]
                                Rate[k, m, c3, i, j, 4] = m
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
                                    Exec_time[k, m, c3, i, j, 1] = descript_time / (10 ** 9)
                                    start_time = time.perf_counter_ns()
                                    Rate[k, m, c3, i, j, 11], good_matches, matches = evaluate_with_fundamentalMat_and_XSAC(m, keypoints1, keypoints2, descriptors1, descriptors2, Normalization[c3])
                                    Exec_time[k, m, c3, i, j, 2] = (time.perf_counter_ns() - start_time) / (10 ** 9)
                                    Rate[k, m, c3, i, j, 5] = len(keypoints1)
                                    Rate[k, m, c3, i, j, 6] = len(keypoints2)
                                    Rate[k, m, c3, i, j, 7] = len(descriptors1)
                                    Rate[k, m, c3, i, j, 8] = len(descriptors2)
                                    Rate[k, m, c3, i, j, 9] = len(good_matches)
                                    Rate[k, m, c3, i, j,10] = len(matches)
                                    Rate[k, m, c3, i, j,12] = (Rate[k, m, c3, i, j, 9] / Rate[k, m, c3, i, j, 5]) if Rate[k, m, c3, i, j, 5] != 0 else 0 # Recall = Inliers / Ground Truth keypoints
                                    Rate[k, m, c3, i, j,13] = (Rate[k, m, c3, i, j, 9] / Rate[k, m, c3, i, j,10]) if Rate[k, m, c3, i, j,10] != 0 else 0 # Precision = Inliers / All Matches
                                    # Rate[k, m, c3, i, j,14] = (Rate[k, m, c3, i, j, 9] / Rate[k, m, c3, i, j, 5]) if Rate[k, m, c3, i, j, 5] != 0 else 0 # Repeatibility = Inliers / Ground Truth keypoints
                                    Rate[k, m, c3, i, j,14] = (Rate[k, m, c3, i, j, 9] / min(Rate[k, m, c3, i, j, 5], Rate[k, m, c3, i, j, 6])) if min(Rate[k, m, c3, i, j, 5], Rate[k, m, c3, i, j, 6]) != 0 else 0 # Repeatibility = Inliers / min(Ground Truth keypoints, Detected keypoints)
                                    Rate[k, m, c3, i, j,15] = (2 * Rate[k, m, c3, i, j,12] * Rate[k, m, c3, i, j,13] / (Rate[k, m, c3, i, j,12] + Rate[k, m, c3, i, j,13])) if Rate[k, m, c3, i, j,12] + Rate[k, m, c3, i, j,13] != 0 else 0 # F1 Score = 2 * Recall * Precision / (Recall + Precision)
                                    Exec_time[k, m, c3, i, j, 3] = Exec_time[k, m, c3, i, j, 0] + Exec_time[k, m, c3, i, j, 1] + Exec_time[k, m, c3, i, j, 2] # Total Execution Time
                                    Exec_time[k, m, c3, i, j, 4] = ((Exec_time[k, m, c3, i, j, 0] / Rate[k, m, c3, i, j, 6]) * 1000) if Rate[k, m, c3, i, j, 6] != 0 else 0 # Detect Time per 1K keypoints
                                    Exec_time[k, m, c3, i, j, 5] = ((Exec_time[k, m, c3, i, j, 1] / Rate[k, m, c3, i, j, 8]) * 1000) if Rate[k, m, c3, i, j, 8] != 0 else 0 # Descript Time per 1K keypoints
                                    Exec_time[k, m, c3, i, j, 6] = ((Exec_time[k, m, c3, i, j, 3] / Rate[k, m, c3, i, j,10]) * 1000) if Rate[k, m, c3, i, j,10] != 0 else 0 # Total Match Time per 1K keypoints
                                    Exec_time[k, m, c3, i, j, 7] = ((Exec_time[k, m, c3, i, j, 3] / Rate[k, m, c3, i, j, 9]) * 1000) if Rate[k, m, c3, i, j, 9] != 0 else 0 # Inliers Total Time per 1K keypoints
                                except:
                                    Exec_time[k, m, c3, i, j, :] = None
                                    Rate[k, m, c3, i, j, 5:16] = None
                                    continue
                                if drawing and k == 3:
                                    img_matches = draw_matches(img[0], keypoints1, img[1], keypoints2, matches, good_matches, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
                                    filename = f"./draws/{folder}/{k}_{method_dtect.getDefaultName().split('.')[-1]}_{method_dscrpt.getDefaultName().split('.')[-1]}_{Normalization[c3]}_{Matcher[m]}.png"
                                    cv2.imwrite(filename, img_matches)
                    else:
                        continue
            else:
                continue
    if save:
        np.save(f"./arrays/Rate_{folder}.npy",      Rate)
        np.save(f"./arrays/Exec_time_{folder}.npy", Exec_time)
        saveAverageCSV(Rate, Exec_time, folder)
        saveAllCSV(Rate, Exec_time, folder)