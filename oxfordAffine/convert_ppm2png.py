import os
from PIL import Image

# Function to convert PPM to PNG
def convert_to_png(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'PNG')
        print(f"Converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error converting {input_file}: {e}")

# Get the current directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Loop through all subdirectories and files in the script's directory
for root, dirs, files in os.walk(script_directory):
    for file in files:
        if file.endswith('.ppm'):
            ppm_path = os.path.join(root, file)
            png_path = ppm_path.replace('.ppm', '.png')
            convert_to_png(ppm_path, png_path)

# Loop through all subdirectories and files in the script's directory
for root, dirs, files in os.walk(script_directory):
    for file in files:
        if file.endswith('.pgm'):
            ppm_path = os.path.join(root, file)
            png_path = ppm_path.replace('.pgm', '.png')
            convert_to_png(ppm_path, png_path)