import cv2
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import imageio as io

colors = [
    [255,255,255],
    [252,244,4],
    [255,100,4],
    [220,8,8],
    [240,8,132],
    [72,0,184],
    [0,0,212],
    [0,172,232],
    [32,184,20],
    [0,100,16],
    [88,44,4],
    [144,112,56],
    [192,192,192],
    [128,128,128],
    [64,64,64],
    [0,0,0]
    ]

def rgb_to_nearest_16(pixel):
    nearest_color = []
    lowest_sum = 765

    for color in colors:
        color_rgb = sRGBColor(color[0], color[1], color[2])
        pixel_rgb = sRGBColor(pixel[0], pixel[1], pixel[2])
        color_lab = convert_color(color_rgb, LabColor)
        pixel_lab = convert_color(pixel_rgb, LabColor)

        sum = delta_e_cie2000(color_lab, pixel_lab)

        if sum <= lowest_sum:
            lowest_sum = sum
            nearest_color = color

    return nearest_color


def make_16(image):
    """Returns the provided image array with the pixels changed to fit
        the 16 color palette"""

    height, width = image.shape[:2]

    for row_index in range(height):
        for col_index in range(width):
            nearest_color = rgb_to_nearest_16(image[row_index][col_index])

            image[row_index][col_index] = np.array(nearest_color)

    return image

    
if __name__ == "__main__":
    image = io.read_image("../images/squared/mike.jpg")
    image = make_16(image)
    io.write_image(image, "../images/final/mike.jpg")