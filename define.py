import cv2
from plotly.colors import sample_colorscale
from plotly.validators.scatter.marker import SymbolValidator
import numpy as np
import csv

val_b    = np.array([-30, -10, 10, 30])     # b ∈ [−30 : 20 : +30]
val_c    = np.array([0.7, 0.9, 1.1, 1.3])   # c ∈ [0.7 : 0.2 : 1.3]
nbre_img = len(val_b) + len(val_c)          # number of intensity change values ==> number of test images
scale    = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]   # s ∈]1.1 : 0.2 : 2.3]
rot      = [15, 30, 45, 60, 75, 90]         # r ∈ [15 : 15 : 90

DetectorsLegend   = ['sift', 'akaze', 'orb', 'brisk', 'kaze', 'fast', 'mser', 'agast', 'gftt', 'gftt_harris', 'star', 'hl', 'msd', 'tbmr']
DescriptorsLegend = ['sift', 'akaze', 'orb', 'brisk', 'kaze', 'daisy', 'freak', 'brief', 'lucid', 'latch', 'vgg', 'beblid', 'teblid', 'boost']
line_styles = ['solid', 'dash', 'dot'] #, 'dashdot']
Norm = ['L2', 'HAM']
Matcher = ['BF', 'Flann']

raw_symbols = SymbolValidator().values
num_combinations = len(DetectorsLegend) * len(DescriptorsLegend)
colors = sample_colorscale('Turbo', [i / num_combinations for i in range(num_combinations)])

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

def match_with_bf_ratio_test(matcher, Dspt1, Dspt2, norm_type, threshold_ratio=0.8):
    if matcher == 0: # Brute-force matcher
        bf = cv2.BFMatcher(norm_type, crossCheck=True) 
        matches = bf.match(Dspt1, Dspt2)
    else: # Flann-based matcher
        if norm_type == cv2.NORM_L2:
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
        elif norm_type == cv2.NORM_HAMMING:
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.match(Dspt1, Dspt2)
    good_matches = []
    for m,n in matches:
        if m.distance < threshold_ratio * n.distance:
            good_matches.append(m)
    good_matches = sorted(good_matches, key = lambda x:x.distance)
    match_rate = (len(good_matches) / len(matches) * 100 if len(matches) > 0 else 0)
    return match_rate, good_matches, matches

def evaluate_with_fundamentalMat_and_XSAC(matcher, KP1, KP2, Dspt1, Dspt2, norm_type):
    if matcher == 0: # Brute-force matcher
        bf = cv2.BFMatcher(norm_type, crossCheck=True) 
        matches = bf.match(Dspt1, Dspt2)
    else: # Flann-based matcher
        if norm_type == cv2.NORM_L2:
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
        elif norm_type == cv2.NORM_HAMMING:
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.match(Dspt1, Dspt2)
    # matchesSorted = sorted(matches, key = lambda x:x.distance)
    # matches = matchesSorted[:1000]               
    points1 = np.array([KP1[match.queryIdx].pt for match in matches], dtype=np.float32)
    points2 = np.array([KP2[match.trainIdx].pt for match in matches], dtype=np.float32)
    
    _, mask = cv2.findFundamentalMat(points1, points2, cv2.USAC_MAGSAC) # MAGSAC++
    inliers = [matches[i] for i in range(len(matches)) if mask[i] == 1]
    # inliers.sort(key=lambda x: x.distance)
    inliers_percentage = ((len(inliers) / len(matches)) * 100 if len(matches) > 0 else 0)
    return inliers_percentage, inliers, matches

def draw_matches(img1, kp1, img2, kp2, total_matches, good_matches, Rate, Exec_time, method_dtect, method_dscrpt, c3, m):
    keypointImage1 = cv2.drawKeypoints(img1, kp1, None, color=( 255,  0, 0), flags=0)
    keypointImage2 = cv2.drawKeypoints(img2, kp2, None, color=( 255,  0, 0), flags=0)
    # Create a blank image with the size of both images combined
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    combined_img = np.zeros((max(h1, h2), w1 + w2, 3), dtype='uint8')
    combined_img[:h1, :w1] = keypointImage1
    combined_img[:h2, w1:w1 + w2] = keypointImage2
    # Create a set of good matches for faster lookup
    good_matches_set = set(good_matches)
    # Draw all lines in a single loop
    for match in total_matches:
        pt1 = tuple(map(int, kp1[match.queryIdx].pt))
        pt2 = tuple(map(int, kp2[match.trainIdx].pt))
        pt2 = (pt2[0] + w1, pt2[1])
        # Check if the match is a good match
        if match in good_matches_set:
            color = (0, 255, 0)  # Green for inliers
        else:
            color = (0, 0, 255)  # Red for outliers
        cv2.line(combined_img, pt1, pt2, color, 1)
    # Metadata On Image    
    text1 = [   "Detector:", "Keypoint1:", "Keypoint2:", "1K Detect Time:",
                "Descriptor:", "Descriptor1:", "Descriptor2:", "1K Descript Time:",
                "Norm.:", "Matcher:", "Match Rate:", "Inliers:", "All Matches:",
                "Total Time:", "1K Match Tot. Time:", "1K Inliers Time:",
                "Recall", "Precision", "Repeatibility", "F1-Score"]
    text2 = [   f"{method_dtect.getDefaultName().split('.')[-1]}",      # Detector
                f"{Rate[5]}",                                           # Keypoint1
                f"{Rate[6]}",                                           # Keypoint2
                f"{Exec_time[4]:.4f}",                                  # 1K Detect Time
                f"{method_dscrpt.getDefaultName().split('.')[-1]}",     # Descriptor
                f"{Rate[7]}",                                           # Descriptor1
                f"{Rate[8]}",                                           # Descriptor2
                f"{Exec_time[5]:.4f}",                                  # 1K Descript Time
                f"{Norm[c3]}",                                          # Matching
                f"{Matcher[m]}",                                        # Matcher
                f"{Rate[11]:.2f}",                                      # Match Rate
                f"{Rate[9]}",                                           # Inliers
                f"{Rate[10]}",                                          # All Matches
                f"{Exec_time[3]:.4f}",                                  # Total Time
                f"{Exec_time[6]:.4f}",                                  # 1K Match Tot. Time
                f"{Exec_time[7]:.4f}",                                  # 1K Inliers Time
                f"{Rate[12]:.4f}",                                      # Recall
                f"{Rate[13]:.4f}",                                      # Precision
                f"{Rate[14]:.4f}",                                      # Repeatibility
                f"{Rate[15]:.4f}"]                                      # F1-Score
    for idx, txt in enumerate(text1):
        cv2.putText(combined_img, txt, (30, 30+idx*22), cv2.FONT_HERSHEY_COMPLEX , 0.6, (198, 198, 198), 2, cv2.LINE_AA)
        cv2.putText(combined_img, txt, (30, 30+idx*22), cv2.FONT_HERSHEY_COMPLEX , 0.6, (  0,   0,   0), 1, cv2.LINE_AA)
    for idx, txt in enumerate(text2):
        cv2.putText(combined_img, txt, (240, 30+idx*22), cv2.FONT_HERSHEY_COMPLEX , 0.6, (198, 198, 198), 2, cv2.LINE_AA)
        cv2.putText(combined_img, txt, (240, 30+idx*22), cv2.FONT_HERSHEY_COMPLEX , 0.6, (  0,   0,   0), 1, cv2.LINE_AA)
    return combined_img

def saveAverageCSV(Rate, Exec_time, scenario):
    headers = [ "Detector", "Keypoint1", "Keypoint2", "1K Detect Time",
                "Descriptor", "Descriptor1", "Descriptor2", "1K Descript Time",
                "Norm.", "Matcher", "Match Rate", "Inliers", "All Matches",
                "Total Time", "1K Match Tot. Time", "1K Inliers Time",
                "Recall", "Precision", "Repeatibility", "F1-Score"]
    with open(f'./csv/{scenario}_analysis.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
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
                                np.nanmean(Rate[:, m, c3, i, j, 11]),         # MATCH RATE
                                np.nanmean(Rate[:, m, c3, i, j,  9]),         # Inliers
                                np.nanmean(Rate[:, m, c3, i, j, 10]),         # All Matches
                                np.nanmean(Exec_time[:, m, c3, i, j, 3]),     # Total Time
                                np.nanmean(Exec_time[:, m, c3, i, j, 6]),     # 1K Match Tot. Time
                                np.nanmean(Exec_time[:, m, c3, i, j, 7]),     # 1K Inliers Time
                                np.nanmean(Rate[:, m, c3, i, j, 12]),         # Recall
                                np.nanmean(Rate[:, m, c3, i, j, 13]),         # Precision
                                np.nanmean(Rate[:, m, c3, i, j, 14]),         # Repeatibility
                                np.nanmean(Rate[:, m, c3, i, j, 15])]         # F1-Score
                        writer.writerow(row)
                    
def saveAllCSV(Rate, Exec_time, scenario):
    headers = [ "k", "Detector", "Keypoint1-GT", "Keypoint2", "Detect Time", "1K Detect Time",
                "Descriptor", "Descriptor1-GT", "Descriptor2", "Descript Time", "1K Descript Time",
                "Norm.", "Matcher", "Match Rate", "Inliers", "All Matches", "Match Time",
                "Total Time", "1K Match Tot. Time", "1K Inliers Time",
                "Recall", "Precision", "Repeatibility", "F1-Score"]
    with open(f'./csv/{scenario}_analysis_all.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
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
                                    Rate[k, m, c3, i, j, 11],               # MATCH RATE
                                    Rate[k, m, c3, i, j,  9],               # Inliers
                                    Rate[k, m, c3, i, j, 10],               # All Matches
                                    Exec_time[k, m, c3, i, j, 2],           # Match Time
                                    Exec_time[k, m, c3, i, j, 3],           # Total Time
                                    Exec_time[k, m, c3, i, j, 6],           # 1K Match Tot. Time
                                    Exec_time[k, m, c3, i, j, 7],           # 1K Inliers Time
                                    Rate[k, m, c3, i, j, 12],               # Recall
                                    Rate[k, m, c3, i, j, 13],               # Precision
                                    Rate[k, m, c3, i, j, 14],               # Repeatibility
                                    Rate[k, m, c3, i, j, 15]]               # F1-Score
                            writer.writerow(row)