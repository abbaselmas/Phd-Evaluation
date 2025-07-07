import cv2
import numpy as np
import time, os
from define import *

def executeUAVScenarios(folder="uav", a=100, b=100, drawing=False, save=True, mobile=""):
    print(time.ctime() + f" {folder} started")
    print(f"Folder: {folder}")
    img = [cv2.imread(f"./Datasets/UAV/{i}.JPG") for i in range(20)]
    Rate      = np.load(f"./arrays/Rate_{folder}{mobile}.npy")      if os.path.exists(f"./arrays/Rate_{folder}{mobile}.npy")      else np.full((int(len(img)/2), 2, len(Normalization), len(Detectors), len(Descriptors), 17), np.nan)
    Exec_time = np.load(f"./arrays/Exec_time_{folder}{mobile}.npy") if os.path.exists(f"./arrays/Exec_time_{folder}{mobile}.npy") else np.full((int(len(img)/2), 2, len(Normalization), len(Detectors), len(Descriptors), 9), np.nan)
    keypoints_cache   = np.empty((len(img), len(Detectors), 2), dtype=object)
    descriptors_cache = np.empty((len(img), len(Detectors), len(Descriptors), 2), dtype=object)
    for n in range(0,len(img), 2): # 0, 2, 4, 6, 8, 10, 12, 14, 16, 18
        if drawing:
            if n != 8:
                continue
        k = int(n/2) # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
        for i in range(len(Detectors)):
            if (i == a or a == 100):
                method_dtect = Detectors[i]
                if keypoints_cache[n, i, 0] is None:
                    keypoints1 = method_dtect.detect(img[n], None)
                    keypoints_cache[n, i, 0] = keypoints1
                else:
                    keypoints1 = keypoints_cache[n, i, 0]
                if keypoints_cache[n+1, i, 1] is None:
                    start_time = time.perf_counter_ns()
                    keypoints2 = method_dtect.detect(img[n+1], None)
                    detect_time = time.perf_counter_ns() - start_time
                    keypoints_cache[n+1, i, 1] = keypoints2
                else:
                    keypoints2 = keypoints_cache[n+1, i, 1]
                for j in range(len(Descriptors)):
                    if j == b or b == 100:
                        method_dscrpt = Descriptors[j]
                        for c3 in range(2): # Normalization Type 0: L2, 1: Hamming
                            for m in range(2): # Matcher 0: BF, 1: FLANN
                                try:
                                    if descriptors_cache[n, i, j, 0] is None:
                                        keypoints1_updated, descriptors1 = method_dscrpt.compute(img[n], keypoints1)
                                        descriptors_cache[n, i, j, 0] = descriptors1
                                    else:
                                        descriptors1 = descriptors_cache[n, i, j, 0]
                                        keypoints1_updated = keypoints_cache[n, i, 0]
                                    if descriptors_cache[n+1, i, j, 1] is None:
                                        start_time = time.perf_counter_ns()
                                        keypoints2_updated, descriptors2 = method_dscrpt.compute(img[n+1], keypoints2)
                                        descript_time = time.perf_counter_ns() - start_time
                                        descriptors_cache[n+1, i, j, 1] = descriptors2
                                    else:
                                        descriptors2 = descriptors_cache[n+1, i, j, 1]
                                        keypoints2_updated = keypoints_cache[n+1, i, 1]
                                    start_time = time.perf_counter_ns()
                                    inliers, matches = evaluate_with_fundamentalMat_and_XSAC(m, keypoints1_updated, keypoints2_updated, descriptors1, descriptors2, Normalization[c3])
                                    Exec_time[k, m, c3, i, j, 2] = (time.perf_counter_ns() - start_time) / (10 ** 9)
                                    Rate, Exec_time = process_matches(Rate, Exec_time, k, m, c3, i, j, len(keypoints1), len(keypoints2), len(descriptors1), len(descriptors2), len(inliers), len(matches), detect_time, descript_time)
                                except:
                                    Exec_time[k, m, c3, i, j, :] = None
                                    Rate[k, m, c3, i, j, 5:16] = None
                                    continue
                                if drawing and Rate[k, m, c3, i, j, 13] > 0.5 and Rate[k, m, c3, i, j, 15] > 0.25 and Rate[k, m, c3, i, j, 9] > 725 and Rate[k, m, c3, i, j, 12] > 0.16 and Rate[k, m, c3, i, j, 14] > 0.17 and Exec_time[k, m, c3, i, j, 7] < 0.5 and Exec_time[k, m, c3, i, j, 6] < 0.5:
                                    img_matches = draw_matches(img[n], keypoints1_updated, img[n+1], keypoints2_updated, matches, inliers, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
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