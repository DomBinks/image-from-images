import cv2
import imageio as io

def tint(path, red, green, blue):
    """Returns the provided image array tinted using the value provided"""
    image = io.read_image(path)
    for row in image:
        for col in row:
            col[0] *= blue/255
            col[1] *= green/255
            col[2] *= red/255

    return image

if __name__ == "__main__":
    path = '../images/source/mike.jpg'
    #path = '../images/source/giraffe.jpeg'

    dest = '../images/tinted/mike.jpg'
    #dest = '../images/tinted/giraffe.jpeg'
            
    image = tint(path, 230, 0, 255)
    io.save_image(image, dest)