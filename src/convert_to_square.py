import cv2
import imageio as io

def make_square(image, side_length):
    """Returns a cropped version of the provided image array as a square with sides of the length specified"""

    height, width = image.shape[:2]

    #Landscape image
    if height < width:
        l_offset = height // 2
        r_offset = height // 2

        if height % 2 != 0:
            r_offset += 1

        image = image[0:height, int((int(width / 2) - l_offset)):int((int(width / 2) + r_offset))]

    #Portrait image
    if height > width:
        l_offset = width // 2
        r_offset = width // 2

        if width % 2 != 0:
            r_offset += 1

        image = image[int((int(height / 2) - l_offset)):int((int(height / 2) + r_offset)), 0:width]

    #Resize image to have sides of the length specified
    image = cv2.resize(image, (side_length, side_length))

    return image

if __name__ == "__main__":
    path = '../images/source/mike.jpg'
    dest = '../images/squared/mike.jpg'

    image = io.read_image(path)
    image = make_square(image, 64)
    io.write_image(image, dest)
