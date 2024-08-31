import os
from PIL import Image

def resize_images(input_dir, output_dir, new_width):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)
            width_percent = new_width / float(img.size[0])
            new_height = int((float(img.size[1]) * float(width_percent)))
            img = img.resize((new_width, new_height), Image.LANCZOS)
            output_path = os.path.join(output_dir, filename)
            img.save(output_path, "JPEG")
            print(f"Resized and saved {filename} to {output_path}")

input_directory = 'Small_Buildings/drone'
output_directory = 'Small_Buildings/droneResized'
new_width = 1000

resize_images(input_directory, output_directory, new_width)
