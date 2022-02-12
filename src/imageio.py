import cv2

def read_image(path):
    """Returns an image array corresponding to the file provided"""

    image = cv2.imread(path, 1)
    
    return image

def write_image(image, path):
    """Writes the image array provided at the path provided"""

    cv2.imwrite(path, image)
    
    return

if __name__ == "__main__":
    path = '../images/source/mike.jpg'

    image = read_image(path)
    cv2.imshow('Image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()