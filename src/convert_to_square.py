import cv2

def read_image(path):
    """Returns an image array corresponding to the file provided"""

    image = cv2.imread(path, 1)
    
    return image

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
    
def save_image(image, path):
    """Saves the image array provided at the path provided"""

    cv2.imwrite(path, image)
    
    return

if __name__ == "__main__":
    #path = '../images/source/mike.jpg'
    path = '../images/source/giraffe.jpeg'

    #dest = '../images/squared/mike.jpg'
    dest = '../images/squared/giraffe.jpeg'

    image = read_image(path)
    image = make_square(image, 16)
    save_image(image, dest)

    cv2.imshow('Image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()