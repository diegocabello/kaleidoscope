import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter

size = (1920, 1080)
padding = 50
total_size = tuple(x + (padding * 2) for x in size)

# DARKEN BACKGROUND
def darken_background():
    overlay_path = os.path.join('resources', 'overlay.png')

    overlay_image = Image.new('RGBA', (1920, 1080), color = (0, 0, 0, 40)) # change this if you want to change how dark it is 
    overlay_image.save(overlay_path)

# IMAGE SHADOW (temp)
def create_background_shadow():
    shadow_image_path = os.path.join("resources", 'shadow_unblurred.png')
    blurred_shadow_path = os.path.join("resources", 'shadow_blurred.png')

    image_to_be_blurred = Image.new('RGBA', total_size, color=(0,0,0,0))

    draw = ImageDraw.Draw(image_to_be_blurred)
    x1, y1 = padding, padding
    x2, y2 = x1 + size[0], y1 + size[1]
    draw.rectangle([(x1, y1), (x2, y2)], fill=(0, 0, 0, 255))

    image_to_be_blurred.save(shadow_image_path)
    subprocess.run(shadow_image_path, shell=True)

    shadow_cmd = f'ffmpeg -i {shadow_image_path} -vf "boxblur=25" -frames:v 1 -loglevel warning {blurred_shadow_path}'
    subprocess.run(shadow_cmd, shell=True)
    subprocess.run(blurred_shadow_path, shell=True)

def three():
    shadow_image_path = os.path.join("resources", 'shadow_unblurred.png')

    # Define the dimensions of the image
    width, height = 400, 300

    # Create a transparent background image
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # Draw a black rectangle on the transparent background
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (width - 50, height - 50)], fill="black")

    # Apply Gaussian blur to the black rectangle
    blurred_rectangle = image.filter(ImageFilter.GaussianBlur(radius=10))

    # Save or display the resulting image
    blurred_rectangle.save(shadow_image_path)
    subprocess.run(shadow_image_path, shell=True)

if __name__ == '__main__':
    create_background_shadow()