import cv2, csv
import numpy as np
from plotly.colors import sample_colorscale
import plotly.graph_objs as go

import base64
from PIL import Image
import io
import math

epsilon = 1e-6
val_b    = np.array([-30, -10, 10, 30])     # b ∈ [−30 : 20  : +30]
val_c    = np.array([0.7, 0.9, 1.1, 1.3])   # c ∈ [0.7 : 0.2 : 1.3]
nbre_img = len(val_b) + len(val_c)          # number of intensity change values ==> number of test images
scale    = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]   # s ∈ [1.1 : 0.2 : 2.3]
rot      = [15, 30, 45, 60, 75, 90]         # r ∈ [15  : 15  : 90 ]

DetectorsLegend   = ["sift", "akaze", "orb", "brisk", "kaze", "fast", "mser", "agast", "gftt", "gftt_h", "star", "hl", "msd", "tbmr"]
DescriptorsLegend = ["sift", "akaze", "orb", "brisk", "kaze", "daisy", "freak", "brief", "lucid", "latch", "vgg", "beblid", "teblid", "boost"]
line_styles       = ["solid", "dash", "dot"] #, "dashdot"]
Norm              = ["l2", "ham"]
Matcher           = ["bf", "flann"]

num_combinations = len(DetectorsLegend) * len(DescriptorsLegend)
colors = sample_colorscale("mrybm", [i / num_combinations for i in range(num_combinations)]) #Portland, Turbo, Rainbow, HSV, IceFire, Phase, Electric, Inferno, mrybm
marker_symbols = []
for base in range(14):
    marker_symbols.extend([base, base + 100, base + 200, base + 300])

### detectors/descriptors 5
sift  = cv2.SIFT_create(nfeatures=30000, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10.0, sigma=1.6)
akaze = cv2.AKAZE_create(descriptor_type=cv2.AKAZE_DESCRIPTOR_MLDB, descriptor_size=0, descriptor_channels=3, threshold=0.001, nOctaves=4, nOctaveLayers=4, diffusivity=cv2.KAZE_DIFF_PM_G2, max_points=-1)
orb   = cv2.ORB_create(nfeatures=30000, scaleFactor=1.2, nlevels=6, edgeThreshold=31, firstLevel=0, WTA_K=2, scoreType=cv2.ORB_HARRIS_SCORE, patchSize=31, fastThreshold=20)
brisk = cv2.BRISK_create(thresh=30, octaves=3, patternScale=1.0)
kaze  = cv2.KAZE_create(extended=False, upright=False, threshold=0.003, nOctaves=3, nOctaveLayers=5, diffusivity=cv2.KAZE_DIFF_CHARBONNIER)

### detectors 9
fast  = cv2.FastFeatureDetector_create(nonmaxSuppression=True, type=cv2.FAST_FEATURE_DETECTOR_TYPE_5_8,  threshold=5)
mser  = cv2.MSER_create(delta=5, min_area=20, max_area=2000, max_variation=0.15, min_diversity=0.20, max_evolution=350, area_threshold=1.01, min_margin=0.003, edge_blur_size=5)
agast = cv2.AgastFeatureDetector_create(threshold=20, nonmaxSuppression=True, type=cv2.AGAST_FEATURE_DETECTOR_AGAST_5_8)
gftt  = cv2.GFTTDetector_create(maxCorners=30000, qualityLevel=0.01, minDistance=1.0, blockSize=3, useHarrisDetector=False, k=0.04)
gftt_harris = cv2.GFTTDetector_create(maxCorners=30000, qualityLevel=0.01, minDistance=1.0, blockSize=3, useHarrisDetector=True, k=0.04)
star  = cv2.xfeatures2d.StarDetector_create(maxSize=15, responseThreshold=5, lineThresholdProjected=60, lineThresholdBinarized=30, suppressNonmaxSize=3)
hl    = cv2.xfeatures2d.HarrisLaplaceFeatureDetector_create(numOctaves=3, corn_thresh=0.004, DOG_thresh=0.004, maxCorners=30000, num_layers=2)
msd   = cv2.xfeatures2d.MSDDetector_create(m_patch_radius=3, m_search_area_radius=5, m_nms_radius=5, m_nms_scale_radius=0, m_th_saliency=100.0, m_kNN=4, m_scale_factor=1.25, m_n_scales=-1, m_compute_orientation=0)
tbmr  = cv2.xfeatures2d.TBMR_create(min_area=30, max_area_relative=0.01, scale_factor=1.25, n_scales=2)

### descriptors 9
vgg    = cv2.xfeatures2d.VGG_create(desc=103 ,isigma=1.4, img_normalize=False, use_scale_orientation=True, scale_factor=6.25, dsc_normalize=False)
daisy  = cv2.xfeatures2d.DAISY_create(radius=15, q_radius=3, q_theta=8, q_hist=8, norm=cv2.xfeatures2d.DAISY_NRM_NONE, interpolation=True, use_orientation=False)
freak  = cv2.xfeatures2d.FREAK_create(orientationNormalized=True, scaleNormalized=True, patternScale=20.0, nOctaves=3)
brief  = cv2.xfeatures2d.BriefDescriptorExtractor_create(bytes=16, use_orientation=True)
lucid  = cv2.xfeatures2d.LUCID_create(lucid_kernel=3, blur_kernel=6)
latch  = cv2.xfeatures2d.LATCH_create(bytes=2, rotationInvariance=True, half_ssd_size=1, sigma=1.4)
beblid = cv2.xfeatures2d.BEBLID_create(scale_factor=6.25, n_bits=100)
teblid = cv2.xfeatures2d.TEBLID_create(scale_factor=6.25, n_bits=102)
boost  = cv2.xfeatures2d.BoostDesc_create(desc=100, use_scale_orientation=True, scale_factor=6.25)

Detectors     = list([sift, akaze, orb, brisk, kaze, fast, mser, agast, gftt, gftt_harris, star, hl, msd, tbmr])
#                     0     1      2    3      4     5     6     7      8     9            10    11  12   13
Descriptors   = list([sift, akaze, orb, brisk, kaze, daisy, freak, brief, lucid, latch, vgg, beblid, teblid, boost]) 
#                     0     1      2    3      4     5      6      7      8      9      10   11      12      13
Normalization = list([cv2.NORM_L2, cv2.NORM_HAMMING])

def cross_check_matches(matches1to2, matches2to1):
    matches2to1_set = {(m.trainIdx, m.queryIdx) for m in matches2to1}
    cross_checked_matches = [m for m in matches1to2 if (m.queryIdx, m.trainIdx) in matches2to1_set]
    return cross_checked_matches

def evaluate_with_fundamentalMat_and_XSAC(matcher=0, KP1=None, KP2=None, Dspt1=None, Dspt2=None, norm_type=cv2.NORM_L2):
    if matcher == 0: # Brute-force matcher
        bf = cv2.BFMatcher(norm_type, crossCheck=True) 
        matches = bf.match(Dspt1, Dspt2)
    else: # Flann-based matcher
        if norm_type == cv2.NORM_L2:
            index_params = dict(algorithm=1, trees=5)
        elif norm_type == cv2.NORM_HAMMING:
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches1to2 = flann.match(Dspt1, Dspt2)
        matches2to1 = flann.match(Dspt2, Dspt1)
        matches = cross_check_matches(matches1to2, matches2to1)
    points1 = np.float32([KP1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
    points2 = np.float32([KP2[m.trainIdx].pt for m in matches]).reshape(-1, 2)
    _, mask = cv2.findFundamentalMat(points1, points2, cv2.USAC_MAGSAC) # MAGSAC++
    inliers = [matches[i] for i in range(len(matches)) if mask[i] == 1]
    return inliers, matches

def process_matches(Rate, Exec_time, k, m, c3, i, j, kp1_len, kp2_len, desc1_len, desc2_len, inliers_len, matches_len, detect_time, descript_time):
    Rate[k, m, c3, i, j, 0] = k
    Rate[k, m, c3, i, j, 1] = i
    Rate[k, m, c3, i, j, 2] = j
    Rate[k, m, c3, i, j, 3] = Normalization[c3]
    Rate[k, m, c3, i, j, 4] = m
    Rate[k, m, c3, i, j, 5] = kp1_len
    Rate[k, m, c3, i, j, 6] = kp2_len
    Rate[k, m, c3, i, j, 7] = desc1_len
    Rate[k, m, c3, i, j, 8] = desc2_len
    Rate[k, m, c3, i, j, 9] = inliers_len
    Rate[k, m, c3, i, j, 10] = matches_len
    # Recall = Inliers / Ground Truth keypoints
    Rate[k, m, c3, i, j, 12] = (inliers_len / kp1_len) if kp1_len != 0 else 0
    # Precision = Inliers / All Matches
    Rate[k, m, c3, i, j, 13] = (inliers_len / matches_len) if matches_len != 0 else 0
    # Repeatibility = Inliers / min(Ground Truth keypoints, Detected keypoints)
    Rate[k, m, c3, i, j, 14] = (inliers_len / min(kp1_len, kp2_len)) if min(kp1_len, kp2_len) != 0 else 0
    # F1 Score = 2 * Recall * Precision / (Recall + Precision)
    Rate[k, m, c3, i, j, 15] = (2 * Rate[k, m, c3, i, j, 12] * Rate[k, m, c3, i, j, 13] / (Rate[k, m, c3, i, j, 12] + Rate[k, m, c3, i, j, 13])) if Rate[k, m, c3, i, j, 12] + Rate[k, m, c3, i, j, 13] != 0 else 0
    # Detect time
    Exec_time[k, m, c3, i, j, 0] = detect_time / (10 ** 9)
    # Descriptor time
    Exec_time[k, m, c3, i, j, 1] = descript_time / (10 ** 9)
    # Total Execution Time
    Exec_time[k, m, c3, i, j, 3] = Exec_time[k, m, c3, i, j, 0] + Exec_time[k, m, c3, i, j, 1] + Exec_time[k, m, c3, i, j, 2]
    # Detect Time per 1K keypoints
    Exec_time[k, m, c3, i, j, 4] = ((Exec_time[k, m, c3, i, j, 0] / kp2_len) * 1000) if kp2_len != 0 else 0
    # Descript Time per 1K keypoints
    Exec_time[k, m, c3, i, j, 5] = ((Exec_time[k, m, c3, i, j, 1] / desc2_len) * 1000) if desc2_len != 0 else 0
    # Total Match Time per 1K keypoints
    Exec_time[k, m, c3, i, j, 6] = ((Exec_time[k, m, c3, i, j, 3] / matches_len) * 1000) if matches_len != 0 else 0
    # Inliers Total Time per 1K keypoints
    Exec_time[k, m, c3, i, j, 7] = ((Exec_time[k, m, c3, i, j, 3] / inliers_len) * 1000) if inliers_len != 0 else 0
    return Rate, Exec_time

def draw_metadata(combined_img, Rate, Exec_time, method_dtect, method_dscrpt, c3, m, scenario=""):
    text1 = [   "Combination: ",
                "Keypoints: ",
                "Descriptors: ",
                "Inliers: ",
                "All Matches: ",
                "",
                "1K Match time: ",
                "1K Inliers time: ",
                "",
                "Recall: ",
                "Precision: ",
                "Repeatibility: ",
                "F1-Score: "]
    text2 = [   f"{method_dtect.getDefaultName().split('.')[-1]} {method_dscrpt.getDefaultName().split('.')[-1]} {Norm[c3]} {Matcher[m]}",
                f"{Rate[5]} {Rate[6]}", # Keypoint1-2
                f"{Rate[7]} {Rate[8]}", # Descriptor1-2
                f"{Rate[9]}",           # Inliers
                f"{Rate[10]}",          # All Matches
                f"",
                f"{Exec_time[6]:.4f}",  # 1K Match Tot. Time
                f"{Exec_time[7]:.4f}",  # 1K Inliers Time
                f"",
                f"{Rate[12]:.4f}",      # Recall
                f"{Rate[13]:.4f}",      # Precision
                f"{Rate[14]:.4f}",      # Repeatibility
                f"{Rate[15]:.4f}"]      # F1-Score
    
    if scenario == "drone":
        text1.extend(["", "Reconst. time: ", "Reproject. Err.: ", "3D Points: "])
        text2.extend([  f"",
                        f"{Exec_time[8]:.4f}",  # Reconstruction Time
                        f"{Rate[11]:.4f}",      # Reprojection Error
                        f"{Rate[16]}"])         # 3D Points Count
    
    for idx, txt in enumerate(text1):
        cv2.putText(combined_img, txt, (  30, 40+idx*35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.putText(combined_img, txt, (  30, 40+idx*35), cv2.FONT_HERSHEY_SIMPLEX, 1, (  0,   0,   0), 2, cv2.LINE_AA)
    for idx, txt in enumerate(text2):
        cv2.putText(combined_img, txt, ( 300, 40+idx*35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.putText(combined_img, txt, ( 300, 40+idx*35), cv2.FONT_HERSHEY_SIMPLEX, 1, (  0,   0,   0), 2, cv2.LINE_AA)
    return combined_img

def draw_keypoints(img1, kp1, img2, kp2, method_dtect):
    combined_image = cv2.drawMatches(img1, kp1, img2, kp2, [], None, flags = 4)
    cv2.putText(combined_image, f"{method_dtect.getDefaultName().split('.')[-1]}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.putText(combined_image, f"{method_dtect.getDefaultName().split('.')[-1]}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (  0,   0,   0), 2, cv2.LINE_AA)
    cv2.putText(combined_image, f"Keypoints1: {len(kp1)}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.putText(combined_image, f"Keypoints1: {len(kp1)}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (  0,   0,   0), 2, cv2.LINE_AA)
    cv2.putText(combined_image, f"Keypoints2: {len(kp2)}", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.putText(combined_image, f"Keypoints2: {len(kp2)}", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (  0,   0,   0), 2, cv2.LINE_AA)
    return combined_image

def draw_matches(img1, kp1, img2, kp2, total_matches, inliers, Rate, Exec_time, method_dtect, method_dscrpt, c3, m, scenario=""):
    inliers_set = set(inliers)
    outliers = [match for match in total_matches if match not in inliers_set]
    # inliers = sorted(inliers, key = lambda x:x.distance)
    # outliers = sorted(outliers, key = lambda x:x.distance)
    step = 10 if len(total_matches) > 500 else 5
    img1 = cv2.drawKeypoints(img1, kp1[::step], None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img2 = cv2.drawKeypoints(img2, kp2[::step], None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #first draw inliers
    draw_params1 = dict( matchColor = (66, 252, 28), flags = 2|4)
    combined_img = cv2.drawMatches(img1, kp1, img2, kp2, inliers[::step], None, **draw_params1)
    # # #second draw outliers
    draw_params2 = dict( matchColor = (39, 0, 255), flags = 1|2)
    cv2.drawMatches(img1, kp1, img2, kp2, outliers[::step], combined_img, **draw_params2)

    combined_img = draw_metadata(combined_img, Rate, Exec_time, method_dtect, method_dscrpt, c3, m, scenario)
    return combined_img

def saveAverageCSV(Rate, Exec_time, scenario, mobile=""):
    headers = [ "Detector", "Keypoint1", "Keypoint2", "1K Detect Time",
                "Descriptor", "Descriptor1", "Descriptor2", "1K Descript Time",
                "Norm.", "Matcher", "Inliers", "All Matches",
                "Total Time", "1K Match Tot. Time", "1K Inliers Time",
                "Recall", "Precision", "Repeatibility", "F1-Score"]
    if scenario == "drone":
        headers.extend(["Reprojection Error", "3DPoints", "Reconstruction Time"])
    with open(f"./csv/{scenario}_analysis{mobile}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(headers)
        for m in range(Rate.shape[1]):
            for c3 in range(Rate.shape[2]):
                for i in range(Rate.shape[3]):
                    for j in range(Rate.shape[4]):
                        row = [ DetectorsLegend[i],                           # DETECTOR
                                np.nanmean(Rate[:, m, c3, i, j, 5]),          # Keypoint1
                                np.nanmean(Rate[:, m, c3, i, j, 6]),          # Keypoint2
                                np.nanmean(Exec_time[:, m, c3, i, j, 4]),     # 1K Detect Time
                                DescriptorsLegend[j],                         # DESCRIPTOR
                                np.nanmean(Rate[:, m, c3, i, j, 7]),          # Descriptor1
                                np.nanmean(Rate[:, m, c3, i, j, 8]),          # Descriptor2
                                np.nanmean(Exec_time[:, m, c3, i, j, 5]),     # 1K Descript Time
                                Norm[c3],                                     # Norm
                                Matcher[m],                                   # Matcher
                                np.nanmean(Rate[:, m, c3, i, j,  9]),         # Inliers
                                np.nanmean(Rate[:, m, c3, i, j, 10]),         # All Matches
                                np.nanmean(Exec_time[:, m, c3, i, j, 3]),     # Total Time
                                np.nanmean(Exec_time[:, m, c3, i, j, 6]),     # 1K Match Tot. Time
                                np.nanmean(Exec_time[:, m, c3, i, j, 7]),     # 1K Inliers Time
                                np.nanmean(Rate[:, m, c3, i, j, 12]),         # Recall
                                np.nanmean(Rate[:, m, c3, i, j, 13]),         # Precision
                                np.nanmean(Rate[:, m, c3, i, j, 14]),         # Repeatibility
                                np.nanmean(Rate[:, m, c3, i, j, 15])         # F1-Score
                                ]
                        if scenario == "drone":
                            row.extend([
                                np.nanmean(Rate[:, m, c3, i, j, 11]),         # Reprojection Error
                                np.nanmean(Rate[:, m, c3, i, j, 16]),         # 3D Points Count
                                np.nanmean(Exec_time[:, m, c3, i, j, 8])      # Reconstruction Time
                            ])
                        writer.writerow(row)
                    
def saveAllCSV(Rate, Exec_time, scenario, mobile=""):
    headers = [ "k", "Detector", "Keypoint1-GT", "Keypoint2", "Detect Time", "1K Detect Time",
                "Descriptor", "Descriptor1-GT", "Descriptor2", "Descript Time", "1K Descript Time",
                "Norm.", "Matcher", "Inliers", "All Matches", "Match Time",
                "Total Time", "1K Match Tot. Time", "1K Inliers Time",
                "Recall", "Precision", "Repeatibility", "F1-Score"]
    if scenario == "drone":
        headers.extend(["Reprojection Error", "3D Points", "Reconstruction Time"])
    
    with open(f"./csv/{scenario}_analysis_all{mobile}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(headers)
        for k in range(Rate.shape[0]):
            for m in range(Rate.shape[1]):
                for c3 in range(Rate.shape[2]):
                    for i in range(Rate.shape[3]):
                        for j in range(Rate.shape[4]):
                            row = [ k,                                      # k
                                    DetectorsLegend[i],                     # DETECTOR
                                    Rate[k, m, c3, i, j, 5],                # Keypoint1-GT
                                    Rate[k, m, c3, i, j, 6],                # Keypoint2
                                    Exec_time[k, m, c3, i, j, 0],           # Detect Time
                                    Exec_time[k, m, c3, i, j, 4],           # 1K Detect Time
                                    DescriptorsLegend[j],                   # DESCRIPTOR
                                    Rate[k, m, c3, i, j, 7],                # Descriptor1-GT
                                    Rate[k, m, c3, i, j, 8],                # Descriptor2
                                    Exec_time[k, m, c3, i, j, 1],           # Descript Time
                                    Exec_time[k, m, c3, i, j, 5],           # 1K Descipt Time
                                    Norm[c3],                               # Norm
                                    Matcher[m],                             # Matcher
                                    Rate[k, m, c3, i, j,  9],               # Inliers
                                    Rate[k, m, c3, i, j, 10],               # All Matches
                                    Exec_time[k, m, c3, i, j, 2],           # Match Time
                                    Exec_time[k, m, c3, i, j, 3],           # Total Time
                                    Exec_time[k, m, c3, i, j, 6],           # 1K Match Tot. Time
                                    Exec_time[k, m, c3, i, j, 7],           # 1K Inliers Time
                                    Rate[k, m, c3, i, j, 12],               # Recall
                                    Rate[k, m, c3, i, j, 13],               # Precision
                                    Rate[k, m, c3, i, j, 14],               # Repeatibility
                                    Rate[k, m, c3, i, j, 15]                # F1-Score
                                    ]
                            if scenario == "drone":
                                row.extend([
                                    Rate[k, m, c3, i, j, 11],               # Reprojection Error
                                    Rate[k, m, c3, i, j, 16],               # 3D Points Count
                                    Exec_time[k, m, c3, i, j, 8]            # Reconstruction Time
                                ])
                            writer.writerow(row)

def nonlinear_normalize(value, data, alpha=0.5):
    is_valid_input = ~np.isnan(value) & (value != 0)
    data_for_range = data[~np.isnan(data) & (data != 0)]
    if len(data_for_range) == 0:
        return np.zeros_like(value, dtype=float)
    min_val = np.min(data_for_range)
    max_val = np.max(data_for_range)
    if min_val == max_val:
        return np.where(is_valid_input, 1.0, np.nan)
    result = np.full_like(value, np.nan, dtype=float)
    result[is_valid_input] = ((value[is_valid_input] - min_val) / (max_val - min_val)) ** alpha
    return result

def update_csv_with_efficiency_scores(scenario="drone"):
    try:
        scores = np.load(f"./arrays/Scores_{scenario}.npy")
        csv_path = f"./csv/{scenario}_analysis.csv"
        with open(csv_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            rows = list(reader)
        for row_idx in range(1, len(rows)):  # Skip header row
            for m in range(len(Matcher)):
                for c3 in range(len(Norm)):
                    for i in range(len(DetectorsLegend)):
                        for j in range(len(DescriptorsLegend)):
                            # Check if current row matches the combination
                            if (rows[row_idx][0] == DetectorsLegend[i] and  # Detector
                                rows[row_idx][4] == DescriptorsLegend[j] and  # Descriptor
                                rows[row_idx][8] == Norm[c3] and  # Norm
                                rows[row_idx][9] == Matcher[m]):  # Matcher
                                
                                score = scores[i, j, c3, m]
                                # Check if 'Efficiency' column exists in header
                                if len(rows[0]) > 0 and 'Efficiency' not in rows[0]:
                                    # Add 'Efficiency' to header
                                    rows[0].append('Efficiency')

                                # Ensure row has enough columns for efficiency score
                                while len(rows[row_idx]) < len(rows[0]):
                                    rows[row_idx].append('')

                                # Add or update efficiency score in the last column
                                rows[row_idx][-1] = f"{score:.6f}"
                                break
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(rows)
        print(f"Efficiency scores updated in {csv_path}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error updating efficiency scores: {e}")

def plotly_static_match_viewer( img1, kp1, img2, kp2, matches, inliers,
                                Rate=None, Exec_time=None, method_dtect=None, method_dscrpt=None,
                                c3=0, matcher_index=0, scenario="",
                                detector_index=None, descriptor_index=None, image_index=None,
                                top_n_list=[50, 100, 500, 1000]):
    
    def cv2_to_base64(img):
        pil_img = Image.fromarray(img)
        buff = io.BytesIO()
        pil_img.save(buff, format="PNG")
        return base64.b64encode(buff.getvalue()).decode("utf-8")

    def get_log_step_size(num_matches, base=500, min_step=1, max_step=50):
        if num_matches <= base:
            return min_step
        step = int(math.log2(num_matches / base) * 5 + min_step)
        return min(max(step, min_step), max_step)

    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    h = max(h1, h2)
    combined = np.zeros((h, w1 + w2, 3), dtype=np.uint8)
    combined[:h1, :w1] = img1_rgb
    combined[:h2, w1:] = img2_rgb
    img_base64 = 'data:image/png;base64,' + cv2_to_base64(combined)

    all_traces = []
    visibility = []
    inliers_set = set(inliers)
    trace_labels = []

    modes = ["All", "Inliers", "Outliers"]
    for mode in modes:
        if mode == "All":
            subset = matches
        elif mode == "Inliers":
            subset = [m for m in matches if m in inliers_set]
        elif mode == "Outliers":
            subset = [m for m in matches if m not in inliers_set]

        x_pts, y_pts, colors, hovers, traces = [], [], [], [], []
        for match in subset:
            pt1 = kp1[match.queryIdx].pt
            pt2 = kp2[match.trainIdx].pt
            pt2 = (pt2[0] + w1, pt2[1])
            color = 'rgb(28, 252, 66)' if match in inliers_set else 'rgb(255, 0, 39)'

            traces.append(go.Scatter(x=[pt1[0], pt2[0]], y=[pt1[1], pt2[1]], mode='lines', line=dict(color=color, width=1), hoverinfo='skip', showlegend=False))
            x_pts += [pt1[0], pt2[0]]
            y_pts += [pt1[1], pt2[1]]
            colors += [color, color]
            hovers += [f"Q:{match.queryIdx}<br>D:{match.distance:.2f}", f"T:{match.trainIdx}<br>D:{match.distance:.2f}"]
        traces.append(go.Scatter(x=x_pts, y=y_pts, mode='markers', marker=dict(size=4, color=colors), text=hovers, hoverinfo='text', showlegend=False))
        all_traces.extend(traces)
        visibility.append([True]*len(traces))
        trace_labels.append(mode)

    for n in top_n_list:
        subset = sorted(matches, key=lambda m: m.distance)[:n]
        x_pts, y_pts, colors, hovers, traces = [], [], [], [], []
        for match in subset:
            pt1 = kp1[match.queryIdx].pt
            pt2 = kp2[match.trainIdx].pt
            pt2 = (pt2[0] + w1, pt2[1])
            color = 'rgb(28, 252, 66)' if match in inliers_set else 'rgb(255, 0, 39)'

            traces.append(go.Scatter(x=[pt1[0], pt2[0]], y=[pt1[1], pt2[1]], mode='lines', line=dict(color=color, width=1), hoverinfo='skip', showlegend=False))
            x_pts += [pt1[0], pt2[0]]
            y_pts += [pt1[1], pt2[1]]
            colors += [color, color]
            hovers += [f"Q:{match.queryIdx}<br>D:{match.distance:.2f}", f"T:{match.trainIdx}<br>D:{match.distance:.2f}"]
        traces.append(go.Scatter(x=x_pts, y=y_pts, mode='markers', marker=dict(size=4, color=colors), text=hovers, hoverinfo='text', showlegend=False))
        all_traces.extend(traces)
        visibility.append([True]*len(traces))
        trace_labels.append(f"Top {n}")

    step = get_log_step_size(len(matches))
    subset = matches[::step]
    x_pts, y_pts, colors, hovers, traces = [], [], [], [], []
    for match in subset:
        pt1 = kp1[match.queryIdx].pt
        pt2 = kp2[match.trainIdx].pt
        pt2 = (pt2[0] + w1, pt2[1])
        color = 'rgb(28, 252, 66)' if match in inliers_set else 'rgb(255, 0, 39)'
        traces.append(go.Scatter(x=[pt1[0], pt2[0]], y=[pt1[1], pt2[1]], mode='lines', line=dict(color=color, width=1), hoverinfo='skip', showlegend=False))
        x_pts += [pt1[0], pt2[0]]
        y_pts += [pt1[1], pt2[1]]
        colors += [color, color]
        hovers += [f"Q:{match.queryIdx}<br>D:{match.distance:.2f}", f"T:{match.trainIdx}<br>D:{match.distance:.2f}"]
    traces.append(go.Scatter(x=x_pts, y=y_pts, mode='markers', marker=dict(size=4, color=colors), text=hovers, hoverinfo='text', showlegend=False))
    all_traces.extend(traces)
    visibility.append([True]*len(traces))
    trace_labels.append("Auto Sampled (log-step)")

    all_visibilities = []
    for i in range(len(trace_labels)):
        vis = []
        for j in range(len(trace_labels)):
            vis += [i == j] * len(visibility[j])
        all_visibilities.append(vis)

    dropdown_buttons = []
    for i, label in enumerate(trace_labels):
        dropdown_buttons.append(dict(label=label, method='update', args=[{'visible': all_visibilities[i]}]))

    annotations = []
    if Rate is not None and Exec_time is not None and method_dtect is not None and method_dscrpt is not None:
        text1 = [ "Combination:", "Keypoints:", "Descriptors:", "Inliers:", "All Matches:", "",
                  "1K Match time:", "1K Inliers time:", "",
                  "Recall:", "Precision:", "Repeatibility:", "F1-Score:" ]
        text2 = [ f"{method_dtect.getDefaultName().split('.')[-1]} {method_dscrpt.getDefaultName().split('.')[-1]} {Norm[c3]} {Matcher[matcher_index]}",
                  f"{Rate[5]} {Rate[6]}", f"{Rate[7]} {Rate[8]}", f"{Rate[9]}", f"{Rate[10]}", "",
                  f"{Exec_time[6]:.4f}", f"{Exec_time[7]:.4f}", "",
                  f"{Rate[12]:.4f}", f"{Rate[13]:.4f}", f"{Rate[14]:.4f}", f"{Rate[15]:.4f}"]
        if scenario == "drone":
            text1 += ["", "Reconstruction time:", "Reprojection Error:", "3D Points:"]
            text2 += ["", f"{Exec_time[8]:.4f}", f"{Rate[11]:.4f}", f"{Rate[16]}"]
        for i, (t1, t2) in enumerate(zip(text1, text2)):
            if t1.strip() == "" and t2.strip() == "":
                continue
            annotations.append(dict(
                xref="paper", yref="paper",
                x=0.01, xanchor="left", y=0.97 - i * 0.055, yanchor="top",
                text=f"<b>{t1}</b> {t2}",
                showarrow=False, align="left",
                font=dict(size=22, color="white", family="monospace"),
                bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(255,255,255,0.3)",
                borderpad=4, borderwidth=1, opacity=0.9
            ))

    fig = go.Figure(data=all_traces, layout=go.Layout(
        images=[dict(source=img_base64, xref="x", yref="y", x=0, y=0, sizex=combined.shape[1], sizey=combined.shape[0], sizing="stretch", layer="below")],
        xaxis=dict(range=[0, combined.shape[1]], visible=False),
        yaxis=dict(range=[combined.shape[0], 0], visible=False),
        margin=dict(l=0, r=0, t=30, b=0),
        updatemenus=[dict(buttons=dropdown_buttons, direction="down", x=0, y=1, xanchor="left", yanchor="bottom")],
        width=combined.shape[1],
        height=combined.shape[0],
        annotations=annotations
    ))

    # Save as static HTML file
    if method_dtect is not None and method_dscrpt is not None and detector_index is not None and descriptor_index is not None:
        # Generate filename similar to the PNG version but for HTML
        if image_index is not None:
            html_filename = f"./draws/{scenario}/{image_index}_{detector_index}{method_dtect.getDefaultName().split('.')[-1]}_{descriptor_index}{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[matcher_index]}.html"
        else:
            html_filename = f"./draws/{scenario}/match_viewer_{detector_index}{method_dtect.getDefaultName().split('.')[-1]}_{descriptor_index}{method_dscrpt.getDefaultName().split('.')[-1]}_{Norm[c3]}_{Matcher[matcher_index]}.html"
        fig.write_html(html_filename, include_plotlyjs="cdn", full_html=True)