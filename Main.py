import os
import Lib  # pastikan file Lib.py ada di direktori yang sama atau di PYTHONPATH

image_folder = "Image"  # ganti dengan nama foldermu

# Filter hanya file gambar dengan ekstensi yang sesuai
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

for filename in os.listdir(image_folder):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        image_path = os.path.join(image_folder, filename)
        print(f"\nMemproses: {filename}")
        Lib.detect_black_dots(image_path, 'image')
