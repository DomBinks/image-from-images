import cv2
import imageio as io
import pandas


def tint(image, red, green, blue):
    """Returns the provided image array tinted using the value provided"""
    for row in image:
        for col in row:
            col[0] *= blue/255
            col[1] *= green/255
            col[2] *= red/255

    return image

if __name__ == "__main__":
    path = '../images/source/mike.jpg'
    dest = '../images/tinted/mike.jpg'
            
    image = io.read_image(path)
    image = tint(image, 230, 0, 255)
    io.write_image(image, dest)