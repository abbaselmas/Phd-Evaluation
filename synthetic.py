import cv2
import numpy as np
import time, os
from define import *

hpatches_sequences = ["bird", "colors", "dogman", "tempera", "woman", "wormhole", "yard"]
selected_image = hpatches_sequences[4]
Image = np.array(cv2.imread(f"./Datasets/hpatches-sequences/v_{selected_image}/1.jpg"))

## Scenario 1 (Intensity): Function that returns 8 images with intensity changes from an I image.
def get_intensity_8Img(Img, val_b, val_c): # val_b, val_c must be 2 vectors with 4 values each
    image = np.array(Img, dtype=np.uint16)   # transformation of the image into uint16 so that each pixel of the
                                                # image will have the same intensity change (min value = 0, max value = 65535)
    I0 = np.zeros((image.shape[0], image.shape[1], image.shape[2])) # creation of empty image of 3 chanels to fill it afterwards
    List8Img = list([I0, I0, I0, I0, I0, I0, I0, I0]) # list of our 8 images that we will create
    for i in range(len(val_b)): # for I + b, with: b ∈ [-30 : 20 : +30]
        I =  image + val_b[i]
        List8Img[i] = I.astype(int)
        List8Img[i][List8Img[i] > 255] = 255 # set pixels with intensity > 255 to 255
        List8Img[i][List8Img[i] < 0] = 0 # set the pixels with intensity < 0 to the value of 0
        List8Img[i] = np.array(List8Img[i], dtype=np.uint8) # image transformation to uint8
        filename = f"./Datasets/synthetic/{selected_image}-intensity-image_I+{val_b[i]}.png"
        cv2.imwrite(filename, List8Img[i])
    for j in range(len(val_c)): # for I ∗ c, with: c ∈ [0.7 : 0.2 : 1.3]
        I =  image * val_c[j]
        List8Img[j+4] = I.astype(int)
        List8Img[j+4][List8Img[j+4] > 255] = 255 # set pixels with intensity > 255 to 255
        List8Img[j+4][List8Img[j+4] < 0] = 0 # set the pixels with intensity < 0 to the value of 0
        List8Img[j+4] = np.array(List8Img[j+4], dtype=np.uint8) # transform image to uint8 (min value = 0, max value = 255)
        filename = f"./Datasets/synthetic/{selected_image}-intensity-image_Ix{val_c[j]}.png"
        cv2.imwrite(filename, List8Img[j+4])
    return Img, List8Img
## Scenario 2 (Scale): Function that takes as input the index of the camera, the index of the image n, and a scale, it returns a couple (I, Iscale). In the following, we will work with 7 images with a scale change Is : s ∈]1.1 : 0.2 : 2.3].
def get_cam_scale(Img, s):
    ImgScale = cv2.resize(Img, (0, 0), fx=s, fy=s, interpolation = cv2.INTER_NEAREST) # opencv resize function with INTER_NEAREST interpolation
    I_Is = list([Img, ImgScale]) # list of 2 images (original image and scaled image)
    filename = f"./Datasets/synthetic/{selected_image}-scale-image_{s}.png"
    cv2.imwrite(filename, ImgScale)
    return I_Is
## Scenario 3 (Rotation): Function that takes as input the index of the camera, the index of the image n, and a rotation angle, it returns a couple (I, Irot), and the rotation matrix. In the following, we will work with 9 images with a change of scale For an image I, we will create 9 images (I10, I20...I90) with change of rotation from 10 to 90 with a step of 10.
def get_cam_rot(Img, rotationAngle):
    height, width = Img.shape[:2]
    image_center = (width/2, height/2)
    # Get the rotation matrix
    rotation_mat = cv2.getRotationMatrix2D(image_center, rotationAngle, 1.)
    # Calculate the new bounds of the image
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    # Adjust the rotation matrix to account for translation
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]
    # Perform the actual rotation and obtain the rotated image
    rotated_image = cv2.warpAffine(Img, rotation_mat, (bound_w, bound_h))
    couple_I_Ir = [Img, rotated_image]  # list of 2 images (original image and rotated image)
    # save the rotated image
    filename = f"./Datasets/synthetic/{selected_image}-rotation-image_{rotationAngle}.png"
    cv2.imwrite(filename, rotated_image)
    return couple_I_Ir

def execute_scenario_intensity (a=100, b=100, drawing=False, save=True, mobile=""):
    print(time.ctime() + " Intensity started")
    print("Scenario 1 Intensity")
    Rate      = np.load(f"./arrays/Rate_intensity{mobile}.npy")      if os.path.exists(f"./arrays/Rate_intensity{mobile}.npy")      else np.full((nbre_img, 2, len(Normalization), len(Detectors), len(Descriptors), 17), np.nan)
    Exec_time = np.load(f"./arrays/Exec_time_intensity{mobile}.npy") if os.path.exists(f"./arrays/Exec_time_intensity{mobile}.npy") else np.full((nbre_img, 2, len(Normalization), len(Detectors), len(Descriptors), 8), np.nan)
    keypoints_cache     = np.empty((nbre_img, len(Detectors), 2), dtype=object)
    descriptors_cache   = np.empty((nbre_img, len(Detectors), len(Descriptors), 2), dtype=object)
    img, List8Img = get_intensity_8Img(Image, val_b, val_c)
    for k in range(nbre_img):
        if drawing:
                if k != 7:
                    continue
        img2 = List8Img[k]
        for i in range(len(Detectors)):
            if i == a or a == 100:
                method_dtect = Detectors[i]
                if keypoints_cache[0, i, 0] is None:
                    keypoints1 = method_dtect.detect(img, None)
                    keypoints_cache[0, i, 0] = keypoints1
                else:
                    keypoints1 = keypoints_cache[0, i, 0]
                if keypoints_cache[k, i, 1] is None:
                    start_time = time.perf_counter_ns()
                    keypoints2 = method_dtect.detect(img2, None)
                    detect_time = time.perf_counter_ns() - start_time
                    keypoints_cache[k, i, 1] = keypoints2
                else:
                    keypoints2 = keypoints_cache[k, i, 1]
                for j in range(len(Descriptors)):
                    if j == b or b == 100:
                        method_dscrpt = Descriptors[j]
                        for c3 in range(2): # Normalization type 0: L2, 1: HAMMING
                            # for m in range(2): # Matching type 0: BruteForce, 1: FlannBased
                                m = 1
                                try:
                                    if descriptors_cache[0, i, j, 0] is None:
                                        _, descriptors1 = method_dscrpt.compute(img, keypoints1)
                                        descriptors_cache[0, i, j, 0] = descriptors1
                                    else:
                                        descriptors1 = descriptors_cache[0, i, j, 0]
                                    if descriptors_cache[k, i, j, 1] is None:
                                        start_time = time.perf_counter_ns()
                                        _, descriptors2 = method_dscrpt.compute(img2, keypoints2)
                                        descript_time = time.perf_counter_ns() - start_time
                                        descriptors_cache[k, i, j, 1] = descriptors2
                                    else:
                                        descriptors2 = descriptors_cache[k, i, j, 1]
                                    start_time = time.perf_counter_ns()
                                    inliers, matches = evaluate_with_fundamentalMat_and_XSAC(m, keypoints1, keypoints2, descriptors1, descriptors2, Normalization[c3])
                                    Exec_time[k, m, c3, i, j, 2] = (time.perf_counter_ns() - start_time) / (10 ** 9)
                                    Rate, Exec_time = process_matches(Rate, Exec_time, k, m, c3, i, j, len(keypoints1), len(keypoints2), len(descriptors1), len(descriptors2), len(inliers), len(matches), detect_time, descript_time)
                                except:
                                    Exec_time[k, m, c3, i, j, :] = None
                                    Rate[k, m, c3, i, j, 5:16] = None
                                    continue
                                if drawing and m == 0: # and Rate[k, m, c3, i, j, 13] > 0.5:
                                    img_matches = draw_matches(img, keypoints1, img2, keypoints2, matches, inliers, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
                                    filename = f"./draws/intensity/{selected_image}_{k}_{i}{method_dtect.getDefaultName().split('.')[-1]}_{j}{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[m]}.png"
                                    cv2.imwrite(filename, img_matches)
                    else:
                        continue
            else:
                continue
    if save:
        np.save(f"./arrays/Rate_intensity{mobile}.npy",      Rate)
        np.save(f"./arrays/Exec_time_intensity{mobile}.npy", Exec_time)
        saveAverageCSV(Rate, Exec_time, "intensity", mobile)
        saveAllCSV(Rate, Exec_time, "intensity", mobile)
    print(time.ctime() + " Intensity finished")

def execute_scenario_scale     (a=100, b=100, drawing=False, save=True, mobile=""):
    print(time.ctime() + " Scale started")
    print("Scenario 2 Scale")
    Rate        = np.load(f"./arrays/Rate_scale{mobile}.npy")          if os.path.exists(f"./arrays/Rate_scale{mobile}.npy")          else np.full((len(scale), 2, len(Normalization), len(Detectors), len(Descriptors), 17), np.nan)
    Exec_time   = np.load(f"./arrays/Exec_time_scale{mobile}.npy")     if os.path.exists(f"./arrays/Exec_time_scale{mobile}.npy")     else np.full((len(scale), 2, len(Normalization), len(Detectors), len(Descriptors), 8), np.nan)
    keypoints_cache   = np.empty((nbre_img, len(Detectors), 2), dtype=object)
    descriptors_cache = np.empty((nbre_img, len(Detectors), len(Descriptors), 2), dtype=object)
    for k in range(len(scale)):
        if drawing:
                if k != 4:
                    continue
        img = get_cam_scale(Image, scale[k])
        for i in range(len(Detectors)):
            if i == a or a == 100:
                method_dtect = Detectors[i]
                if keypoints_cache[0, i, 0] is None:
                    keypoints1 = method_dtect.detect(img[0], None)
                    keypoints_cache[0, i, 0] = keypoints1
                else:
                    keypoints1 = keypoints_cache[0, i, 0]
                if keypoints_cache[k, i, 1] is None:
                    start_time = time.perf_counter_ns()
                    keypoints2 = method_dtect.detect(img[1], None)
                    detect_time = time.perf_counter_ns() - start_time
                    keypoints_cache[k, i, 1] = keypoints2
                else:
                    keypoints2 = keypoints_cache[k, i, 1]
                for j in range(len(Descriptors)):
                    if j == b or b == 100:
                        method_dscrpt = Descriptors[j]
                        for c3 in range(2): # Normalization type 0: L2, 1: HAMMING
                            # for m in range(2): # Matching type 0: BruteForce, 1: FlannBased
                                m = 1
                                try:
                                    if descriptors_cache[0, i, j, 0] is None:
                                        _, descriptors1 = method_dscrpt.compute(img[0], keypoints1)
                                        descriptors_cache[0, i, j, 0] = descriptors1
                                    else:
                                        descriptors1 = descriptors_cache[0, i, j, 0]
                                    if descriptors_cache[k, i, j, 1] is None:
                                        start_time = time.perf_counter_ns()
                                        _, descriptors2 = method_dscrpt.compute(img[1], keypoints2)
                                        descript_time = time.perf_counter_ns() - start_time
                                        descriptors_cache[k, i, j, 1] = descriptors2
                                    else:
                                        descriptors2 = descriptors_cache[k, i, j, 1]
                                    start_time = time.perf_counter_ns()
                                    inliers, matches = evaluate_with_fundamentalMat_and_XSAC(m, keypoints1, keypoints2, descriptors1, descriptors2, Normalization[c3])
                                    Exec_time[k, m, c3, i, j, 2] = (time.perf_counter_ns() - start_time) / (10 ** 9)
                                    Rate, Exec_time = process_matches(Rate, Exec_time, k, m, c3, i, j, len(keypoints1), len(keypoints2), len(descriptors1), len(descriptors2), len(inliers), len(matches), detect_time, descript_time)
                                except:
                                    Exec_time[k, m, c3, i, j, :] = None
                                    Rate[k, m, c3, i, j, 5:16] = None
                                    continue
                                if drawing and m == 0: # and Rate[k, m, c3, i, j, 13] > 0.5:
                                    img_matches = draw_matches(img[0], keypoints1, img[1], keypoints2, matches, inliers, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
                                    filename = f"./draws/scale/{selected_image}_{k}_{i}{method_dtect.getDefaultName().split('.')[-1]}_{j}{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[m]}.png"
                                    cv2.imwrite(filename, img_matches)
                    else:
                        continue
            else:
                continue
    if save:
        np.save(f"./arrays/Rate_scale{mobile}.npy",      Rate)
        np.save(f"./arrays/Exec_time_scale{mobile}.npy", Exec_time)
        saveAverageCSV(Rate, Exec_time, "scale", mobile)
        saveAllCSV(Rate, Exec_time, "scale", mobile)
    print(time.ctime() + " Scale finished")

def execute_scenario_rotation  (a=100, b=100, drawing=False, save=True, mobile=""):
    print(time.ctime() + " Rotation started")
    print("Scenario 3 Rotation")
    Rate          = np.load(f"./arrays/Rate_rot{mobile}.npy")       if os.path.exists(f"./arrays/Rate_rot{mobile}.npy")      else np.full((len(rot), 2, len(Normalization), len(Detectors), len(Descriptors), 17), np.nan)
    Exec_time     = np.load(f"./arrays/Exec_time_rot{mobile}.npy")  if os.path.exists(f"./arrays/Exec_time_rot{mobile}.npy") else np.full((len(rot), 2, len(Normalization), len(Detectors), len(Descriptors), 8), np.nan)
    keypoints_cache   = np.empty((nbre_img, len(Detectors), 2), dtype=object)
    descriptors_cache = np.empty((nbre_img, len(Detectors), len(Descriptors), 2), dtype=object)
    for k in range(len(rot)):
        if drawing:
                if k != 4:
                    continue
        img = get_cam_rot(Image, rot[k])
        for i in range(len(Detectors)):
            if i == a or a == 100:
                method_dtect = Detectors[i]
                if keypoints_cache[0, i, 0] is None:
                    keypoints1 = method_dtect.detect(img[0], None)
                    keypoints_cache[0, i, 0] = keypoints1
                else:
                    keypoints1 = keypoints_cache[0, i, 0] 
                if keypoints_cache[k, i, 1] is None:
                    start_time = time.perf_counter_ns()
                    keypoints2 = method_dtect.detect(img[1], None)
                    detect_time = time.perf_counter_ns() - start_time
                    keypoints_cache[k, i, 1] = keypoints2
                else:
                    keypoints2 = keypoints_cache[k, i, 1]
                for j in range(len(Descriptors)):
                    if j == b or b == 100:
                        method_dscrpt = Descriptors[j]
                        for c3 in range(2): # Normalization type 0: L2, 1: HAMMING
                            # for m in range(2): # Matching type 0: BruteForce, 1: FlannBased
                                m = 1
                                try:
                                    if descriptors_cache[0, i, j, 0] is None:
                                        _, descriptors1 = method_dscrpt.compute(img[0], keypoints1)
                                        descriptors_cache[0, i, j, 0] = descriptors1
                                    else:
                                        descriptors1 = descriptors_cache[0, i, j, 0]
                                    if descriptors_cache[k, i, j, 1] is None:
                                        start_time = time.perf_counter_ns()
                                        _, descriptors2 = method_dscrpt.compute(img[1], keypoints2)
                                        descript_time = time.perf_counter_ns() - start_time
                                        descriptors_cache[k, i, j, 1] = descriptors2
                                    else:
                                        descriptors2 = descriptors_cache[k, i, j, 1]
                                    start_time = time.perf_counter_ns()
                                    inliers, matches = evaluate_with_fundamentalMat_and_XSAC(m, keypoints1, keypoints2, descriptors1, descriptors2, Normalization[c3])
                                    Exec_time[k, m, c3, i, j, 2] = (time.perf_counter_ns() - start_time) / (10 ** 9)
                                    Rate, Exec_time = process_matches(Rate, Exec_time, k, m, c3, i, j, len(keypoints1), len(keypoints2), len(descriptors1), len(descriptors2), len(inliers), len(matches), detect_time, descript_time)
                                except:
                                    Exec_time[k, m, c3, i, j, :] = None
                                    Rate[k, m, c3, i, j, 5:16] = None
                                    continue
                                if drawing and m == 0: # and Rate[k, m, c3, i, j, 13] > 0.5:
                                    img_matches = draw_matches(img[0], keypoints1, img[1], keypoints2, matches, inliers, Rate[k, m, c3, i, j, :], Exec_time[k, m, c3, i, j, :], method_dtect, method_dscrpt, c3, m)
                                    filename = f"./draws/rot/{selected_image}_{k}_{i}{method_dtect.getDefaultName().split('.')[-1]}_{j}{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[m]}.png"
                                    cv2.imwrite(filename, img_matches)
                    else:
                        continue
            else:
                continue
    if save:
        np.save(f"./arrays/Rate_rot{mobile}.npy",      Rate)
        np.save(f"./arrays/Exec_time_rot{mobile}.npy", Exec_time)
        saveAverageCSV(Rate, Exec_time, "rot", mobile)
        saveAllCSV(Rate, Exec_time, "rot", mobile)
    print(time.ctime() + " Rotation finished")