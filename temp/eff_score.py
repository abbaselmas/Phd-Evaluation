import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# --- 1. Load Data ---
df = pd.read_excel('drone_analysis.xlsx', sheet_name='drone_analysis')
print("Excel dosyası 'drone_analysis.xlsx' başarıyla yüklendi.")

column_names_for_metrics = [
    'Precision', 'Recall', 'Repeatibility', 'F1-Score', 'Norm Matches', 
    'Norm Inlier', '1- Norm 1K Total Time', '1-Norm 1K Inlier Time', 'Norm 3D points', 
    '1-Norm Reprojection Err.', '1-Norm Reconstruction T.'
]

# Store Detector and Descriptor columns for final output if they exist
detector_col_exists = 'Detector' in df.columns
descriptor_col_exists = 'Descriptor' in df.columns
original_identifiers = df[['Detector', 'Descriptor', 'Norm.', 'Matcher']].copy()

# --- 2. Prepare Data for CRITIC Method ---
# Select metric columns and convert to float
metric_data = df[column_names_for_metrics].values.astype(float)

# Handle NaN values by replacing them with 0 (or a more suitable imputation strategy if known)
original_nan_count = np.sum(np.isnan(metric_data))
if original_nan_count > 0:
    print(f"\nUyarı: Metrik verilerinde {original_nan_count} adet NaN değer tespit edildi. Bunlar 0 ile değiştirilecek.")
    metric_data = np.nan_to_num(metric_data, nan=0.0)

normalized_df = pd.DataFrame(metric_data, columns=column_names_for_metrics)

print(f"\n{len(column_names_for_metrics)} metrik, {metric_data.shape[0]} algoritma kombinasyonu için kullanılacak.")

# --- 3. Implement CRITIC Method for Unsupervised Weight Calculation ---
def calculate_critic_weights(data_df):
    std_devs = data_df.std() # Standard deviation of each metric
    correlation_matrix = data_df.corr(numeric_only=True)
    conflict_scores = (1 - correlation_matrix.abs()).sum() # Sum of absolute differences from 1
    critic_values = std_devs * conflict_scores
    # Normalize critic_values to get weights that sum to 1
    weights = critic_values / critic_values.sum()
    
    return weights

print("\nAdım 1/2: Metrikler için CRITIC ağırlıkları hesaplanıyor...")
unsupervised_weights = calculate_critic_weights(normalized_df)

print("\nHesaplanan Unsupervised (CRITIC) Metrik Ağırlıkları:")
for metric, weight in unsupervised_weights.items():
    print(f"- {metric}: {weight:.4f}")
print(f"Ağırlıkların Toplamı: {unsupervised_weights.sum():.4f}")


# --- 4. Calculate Unsupervised Efficiency Score for Each Combination ---
# Multiply normalized data by the calculated CRITIC weights
# Each row (algorithm combination) will get a single efficiency score.
unsupervised_efficiency_scores = np.dot(metric_data, unsupervised_weights.values)

# Add scores to a new DataFrame for analysis and output
results_df = pd.DataFrame(unsupervised_efficiency_scores, columns=['Unsupervised Efficiency Score'])

# If original identifiers (Detector/Descriptor) exist, add them
if not original_identifiers.empty:
    results_df = pd.concat([original_identifiers, results_df], axis=1)
    
# Add original metric values to the results_df for full context
results_df = pd.concat([results_df, df[column_names_for_metrics]], axis=1)


# --- 5. Rank and Output Results ---
print("\nAdım 2/2: Algoritma kombinasyonları Unsupervised Efficiency Score'a göre sıralanıyor...")

# Sort in descending order of the efficiency score
results_df_sorted = results_df.sort_values(by='Unsupervised Efficiency Score', ascending=False).reset_index(drop=True)

print("\n--- En Yüksek Unsupervised Efficiency Score'a Sahip En İyi 50 Algoritma Kombinasyonu ---")
# Display top 50 rows, including Detector, Descriptor (if present), and the score
display_cols = ['Unsupervised Efficiency Score'] + column_names_for_metrics
if not original_identifiers.empty:
    display_cols = ['Detector', 'Descriptor'] + display_cols

print(results_df_sorted[display_cols].head(50).to_string(index=False))


output_file_name = 'unsupervised_algorithm_ranking.xlsx'
results_df_sorted.to_excel(output_file_name, index=False)
print(f"\nSıralanmış tüm algoritma kombinasyonları '{output_file_name}' dosyasına kaydedildi.")

print("\nUnsupervised analizin tamamı bitti.")