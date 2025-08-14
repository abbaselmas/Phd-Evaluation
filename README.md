# Overview

This repository contains the experimental framework, datasets links, evaluation outputs and visual analytics used in the PhD thesis:

Towards Efficient 3D Reconstruction from UAV Imagery: Evaluation of OpenCV Feature Detection, Description and Matching Combinations.

The work systematically benchmarks almost all feasible OpenCV detector–descriptor–matcher combinations across Synthetic, Oxford, UAV, AirSim, and Drone and integrates them into a COLMAP / pycolmap sparse reconstruction pipeline. A composite, objectively weighted Efficiency Score balances quality and computational cost (multi‑platform: server vs mobile CPUs) to recommend practical pipelines.

## Key Objectives

- Exhaustive evaluation of OpenCV feature pipelines (detector + descriptor + matcher / distance metric) under UAV constraints.
- Cross-platform timing (mobile vs server) and decoupled detector vs descriptor timing analysis.
- Unified evaluation procedure across datasets without relying on external homographies (fundamental matrix with MAGSAC++).
- Programmatic sparse reconstruction via pycolmap for geometric quality metrics.
- Objective composite Efficiency Score for multi-criteria ranking.
- Open, reproducible research assets (data transformations, plots, arrays, HTML dashboards).

## Main Contributions

1. Largest systematic benchmark of OpenCV feature combinations for UAV reconstruction.
2. Cross-platform timing and inlier-normalized (per 1K inliers) efficiency comparison.
3. Objective multi-weight fusion Efficiency Score (Entropy / PCA / CRITIC / Variance).
4. Integration of alternative OpenCV pipelines into COLMAP workflow via pycolmap.
5. Multi-layer AirSim synthetic acquisition design (grid densities + angle schema).
6. Single‑image controlled synthetic transformation dataset (intensity, scale, rotation).
7. Curated real UAV pair dataset plus full Pix4D sequence benchmark.
8. Interactive Plotly dashboards (timing, correlations, efficiency heatmaps, violin, sparse model visuals).
9. Parameter optimization strategy for fair detector/descriptor comparison.
10. Public release enabling replication and extension.

## Datasets

| Dataset | Role | Notes |
|---------|------|-------|
| Synthetic (single-image transforms) | Controlled robustness tests | Intensity / scale / rotation variations with known transform params |
| Oxford Affine | Standard benchmark | Viewpoint / scale / blur / illumination / JPEG sequences |
| AirSim (Multi-layer & Natural) | Controlled simulated UAV | Varying altitude, overlap, multi-angle & traversal capture |
| UAV (curated pairs) | Real-world variability | Diverse scenes; two images per scenario |
| Drone (Pix4D Small Building) | Full sequence benchmark | Primary reconstruction & efficiency reference |

## Methodology Summary

1. Feature Extraction: All detector–descriptor combinations (including joint methods like SIFT, ORB, BRISK, KAZE, AKAZE) plus separated detectors (FAST, AGAST, GFTT, STAR, MSD, TBMR, MSER, Harris-Laplace) with descriptors (SIFT, DAISY, BRIEF, FREAK, LATCH, LUCID, BOOST, VGG, BEBLID, TEBLID).
2. Matching: BF (Hamming / L2) & FLANN where applicable; cross-check + ratio test (if configured); geometric verification via MAGSAC++ fundamental matrix; inlier mask extraction.
3. Metrics: Keypoint count, matches, inliers, repeatability, precision, recall, F1, execution timings (total, detector, descriptor, matching, inlier-normalized), reprojection error, 3D sparse points.
4. Reconstruction: pycolmap incremental SfM per combination for selected datasets.
5. Weighting & Efficiency Score: Normalize metrics, compute unsupervised weights (Entropy, PCA, CRITIC, Variance), aggregate with fusion strategy to produce composite ranking.
6. Visualization: Plotly interactive HTML (correlation matrices, timing bars, heatmaps, violin, efficiency tables, sparse model comparisons).

## Repository Structure (Simplified)

- `main.py` / pipeline orchestration
- `drone.py`, `uav.py`, `airsim.py`, `synthetic.py`, `oxfordAffine.py` dataset handlers
- `display.py` visualization generation (Plotly / HTML)
- `database.py` COLMAP / SQLite interactions
- `define.py` configuration & enums
- `draws/` per-dataset match visualizations (PNG/HTML)
- `arrays/` cached NumPy metric arrays (timings, rates, scores)
- `html/` published dashboards

## Citation

If you use this work please cite (placeholder BibTeX):

```bibtex
@phdthesis{Elmas2025UAVEfficiency,
  title={Towards Efficient 3D Reconstruction from UAV Imagery: Evaluation of OpenCV Feature Detection, Description and Matching Combinations},
  author={Ammar Abbas Elmas},
  school={PhD Thesis},
  year={2025}
}
```

## Results

## Dataset Links

| Dataset    | Main Page | Variants | Timing | Correlation | Efficiency | Heatmap | Violin |
|------------|-----------|----------|--------|-------------|------------|---------|--------|
| **Synthetic** | [synthetic](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/synthetic.html)    | [synthetic4](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/synthetic4.html), [syntheticAll4](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/syntheticAll4.html)  | [synthetic Timing](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/syntheticTiming.html) / [Mobile](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/syntheticTiming_mobile.html) / [Mobile2](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/syntheticTiming_mobile2.html) | [synthetic Correlation](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/synthetic_Correlation.html)    | [synthetic Efficiency](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/synthetic_Efficiency.html)  | [synthetic Heatmap](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/synthetic_Heatmap.html)    | [synthetic Violin](https://abbaselmas.github.io/Phd-Evaluation/html/synthetic/synthetic_Violin.html)  |
| **Oxford**    | [oxford](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxford.html)             | [oxford9](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxford9.html),          [oxfordAll9](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxfordAll9.html)           | [oxford Timing](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxfordTiming.html) / [Mobile](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxfordTiming_mobile.html) / [Mobile2](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxfordTiming_mobile2.html)  | [oxford Correlation](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxford_Correlation.html)             | [oxford Efficiency](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxford_Efficiency.html)           | [oxford Heatmap](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxford_Heatmap.html)             | [oxford Violin](https://abbaselmas.github.io/Phd-Evaluation/html/oxford/oxford_Violin.html)           |
| **Drone**     | [drone](https://abbaselmas.github.io/Phd-Evaluation/html/drone/drone.html)                | [droneAll](https://abbaselmas.github.io/Phd-Evaluation/html/drone/droneAll.html)                                                                                                          | [drone Timing](https://abbaselmas.github.io/Phd-Evaluation/html/drone/droneTiming.html)                                                                                                                 | [drone Correlation](https://abbaselmas.github.io/Phd-Evaluation/html/drone/drone_Correlation.html)                | [drone Efficiency](https://abbaselmas.github.io/Phd-Evaluation/html/drone/drone_Efficiency.html)              | [drone Heatmap](https://abbaselmas.github.io/Phd-Evaluation/html/drone/drone_Heatmap.html)                | [drone Violin](https://abbaselmas.github.io/Phd-Evaluation/html/drone/drone_Violin.html)              |
| **UAV**       | [uav](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uav.html)                      | [uavAll](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uavAll.html)                                                                                                                | [uavTiming](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uavTiming.html)                                                                                                                        | [uav Correlation](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uav_Correlation.html)                      | [uav Efficiency](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uav_Efficiency.html)                    | [uav Heatmap](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uav_Heatmap.html)                      | [uav Violin](https://abbaselmas.github.io/Phd-Evaluation/html/uav/uav_Violin.html)                    |
| **AirSim**    | [airsim](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsim.html)             | [airsimAll](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsimAll.html)                                                                                                       | [airsimTiming](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsimTiming.html)                                                                                                               | [airsim Correlation](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsim_Correlation.html)             | [airsim Efficiency](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsim_Efficiency.html)           | [airsim Heatmap](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsim_Heatmap.html)             | [airsim Violin](https://abbaselmas.github.io/Phd-Evaluation/html/airsim/airsim_Violin.html)           |

## Recommendations

| Method Combination | PNG | HTML |
|--------------------|-----|------|
|GFTT_H BEBLID|[PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_9GFTT_H_11BEBLID_ham_bf.png)|[HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_9GFTT_H_11BEBLID_ham_bf.html)|
|STAR BEBLID|[PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_10STAR_11BEBLID_ham_bf.png)|[HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_10STAR_11BEBLID_ham_bf.html)|
|AGAST BEBLID|[PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AGAST_11BEBLID_ham_bf.png)|[HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AGAST_11BEBLID_ham_bf.html)|
|ORB BEBLID|[PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_11BEBLID_ham_bf.png)|[HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_11BEBLID_ham_bf.html)|
|GFTT BRISK|[PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTT_3BRISK_l2_bf.png)|[HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTT_3BRISK_l2_bf.html)|
|ORB DAISY|[PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_5DAISY_l2_bf.png)|[HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_5DAISY_l2_bf.html)|

## Combined Detection/Descriptor Visualization Table (Efficiency Top 30)

| Detector-Descriptor Combination | Drone | AirSim | UAV |
|---------------------------------|-------|--------|-----|
| ORB + SIFT | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_0SIFT_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_0SIFT_l2_bf.html) |  |
| ORB + BEBLID (BF) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_11BEBLID_ham_bf.html) |
| ORB + BEBLID (FLANN) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_11BEBLID_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_11BEBLID_ham_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_11BEBLID_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_11BEBLID_ham_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_11BEBLID_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_11BEBLID_ham_flann.html) |
| ORB + TEBLID (BF) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_12TEBLID_ham_bf.html) |
| ORB + TEBLID (FLANN) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_12TEBLID_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_12TEBLID_ham_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_12TEBLID_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_12TEBLID_ham_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_12TEBLID_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_12TEBLID_ham_flann.html) |
| ORB + BOOST | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_13BOOST_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_13BOOST_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_13BOOST_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_13BOOST_ham_bf.html) |  |
| ORB + ORB (BF) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_2ORB_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_2ORB_ham_bf.html) |  | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_2ORB_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_2ORB_ham_bf.html) |
| ORB + ORB (FLANN) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_2ORB_ham_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_2ORB_ham_flann.html) |  |  |
| ORB + BRISK | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_3BRISK_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_3BRISK_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_3BRISK_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_3BRISK_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_3BRISK_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_3BRISK_l2_bf.html) |
| ORB + DAISY (BF) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_5DAISY_l2_bf.html) |
| ORB + DAISY (FLANN) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_5DAISY_l2_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_2ORB_5DAISY_l2_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_5DAISY_l2_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_2ORB_5DAISY_l2_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_5DAISY_l2_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_2ORB_5DAISY_l2_flann.html) |
| BRISK + BEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_3BRISK_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_3BRISK_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_3BRISK_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_3BRISK_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_3BRISK_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_3BRISK_11BEBLID_ham_bf.html) |
| BRISK + DAISY | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_3BRISK_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_3BRISK_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_3BRISK_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_3BRISK_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_3BRISK_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_3BRISK_5DAISY_l2_bf.html) |
| FAST + SIFT | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_0SIFT_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_5FastFeatureDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_5FastFeatureDetector_0SIFT_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_0SIFT_l2_bf.html) |
| FAST + VGG | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_10VGG_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_10VGG_l2_bf.html) |  | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_10VGG_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_10VGG_l2_bf.html) |
| FAST + BEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_5FastFeatureDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_5FastFeatureDetector_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_11BEBLID_ham_bf.html) |
| FAST + TEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_5FastFeatureDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_5FastFeatureDetector_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_12TEBLID_ham_bf.html) |
| FAST + DAISY | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_5FastFeatureDetector_5DAISY_l2_bf.html) |  | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_5FastFeatureDetector_5DAISY_l2_bf.html) |
| AGAST + SIFT | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_0SIFT_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_0SIFT_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_0SIFT_l2_bf.html) |
| AGAST + VGG | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_10VGG_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_10VGG_l2_bf.html) |  | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_10VGG_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_10VGG_l2_bf.html) |
| AGAST + BEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_11BEBLID_ham_bf.html) |
| AGAST + TEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_12TEBLID_ham_bf.html) |
| AGAST + DAISY | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_7AgastFeatureDetector_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_7AgastFeatureDetector_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_7AgastFeatureDetector_5DAISY_l2_bf.html) |
| GFTT + SIFT | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_0SIFT_l2_bf.html) |  | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_0SIFT_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_0SIFT_l2_bf.html) |
| GFTT + VGG | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_10VGG_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_10VGG_l2_bf.html) |  | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_10VGG_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_10VGG_l2_bf.html) |
| GFTT + BEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_11BEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_11BEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_11BEBLID_ham_bf.html) |  |
| GFTT + TEBLID | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_12TEBLID_ham_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_12TEBLID_ham_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_12TEBLID_ham_bf.html) |  |
| GFTT + DAISY (BF) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_5DAISY_l2_bf.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_5DAISY_l2_bf.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_5DAISY_l2_bf.html) |
| GFTT + DAISY (FLANN) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_5DAISY_l2_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/drone/17_8GFTTDetector_5DAISY_l2_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_5DAISY_l2_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/airsim/2_8GFTTDetector_5DAISY_l2_flann.html) | [PNG](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_5DAISY_l2_flann.png), [HTML](https://abbaselmas.github.io/Phd-Evaluation/draws/uav/8_8GFTTDetector_5DAISY_l2_flann.html) |

## Acknowledgements

Supported by TÜBİTAK BİDEB 2211-A National PhD Scholarship Program.

## License

Academic / research use permitted.
