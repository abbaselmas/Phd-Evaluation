import os
from PIL import Image

# Function to convert PPM to JPG
def convert_to_jpg(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'JPEG', quality=100, subsampling=0)
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
            jpg_path = ppm_path.replace('.ppm', '.jpg')
            convert_to_jpg(ppm_path, jpg_path)


# Loop through all subdirectories and files in the script's directory
for root, dirs, files in os.walk(script_directory):
    for file in files:
        if file.endswith('.pgm'):
            ppm_path = os.path.join(root, file)
            jpg_path = ppm_path.replace('.pgm', '.jpg')
            convert_to_jpg(ppm_path, jpg_path)