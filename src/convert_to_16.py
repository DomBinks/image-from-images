import cv2
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import imageio as io
import pandas as pd

def rgb_to_nearest_16(pixel, df_colors):
    nearest_color_index = 100
    lowest_sum = 765

    colors_r = df_colors['r'].to_list()
    colors_g = df_colors['g'].to_list()
    colors_b = df_colors['b'].to_list()
    for i in range(len(colors_b)):
        color_rgb = sRGBColor(colors_r[i], colors_g[i], colors_b[i])
        pixel_rgb = sRGBColor(pixel[0], pixel[1], pixel[2])
        color_lab = convert_color(color_rgb, LabColor)
        pixel_lab = convert_color(pixel_rgb, LabColor)

        sum = delta_e_cie2000(color_lab, pixel_lab)

        if sum <= lowest_sum:
            lowest_sum = sum
            nearest_color_index = i

    nearest_color_row = df_colors.iloc[nearest_color_index]
    
    return nearest_color_row


def make_16(image, df_colors):
    """Returns the provided image array with the pixels changed to fit
        the 16 color palette"""

    height, width = image.shape[:2]

    for row_index in range(height):
        for col_index in range(width):
            nearest_color_row = rgb_to_nearest_16(image[row_index][col_index], df_colors)
            nearest_color = [nearest_color_row['r'], nearest_color_row['g'], nearest_color_row['b']]

            image[row_index][col_index] = np.array(nearest_color)

    return image

    
if __name__ == "__main__":
    image = io.read_image("../images/squared/mike.jpg")
    df_colors = pd.read_csv("../colors.csv")
    image = make_16(image, df_colors)
    io.write_image(image, "../images/final/mike.jpg")