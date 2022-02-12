import cv2
import numpy as np
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

def make_16(image):
    """Returns the provided image array with the pixels changed to fit
        the 16 color palette"""

    for row in image:
        for col in row:
            nearest_color = []
            lowest_sum = 765
            
            for color in colors:
                sum = abs(col[0] - color[0]) + abs(col[1] - color[1]) + abs(col[2] - color[2])
                
                if sum < lowest_sum:
                    lowest_sum = sum
                    nearest_color = color

            col = np.array(nearest_color)
            print(col)

    return image

if __name__ == "__main__":
    image = io.read_image("../images/source/mike.jpg")
    image = make_16(image)
    io.write_image(image, "../images/final/mike.jpg")