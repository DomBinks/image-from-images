import cv2
import numpy as np
from skimage import io

# returns dominant color in an image as RGB values in np array of size 3 [R, G, B]
# input: path to an image file to profile.
# Uses k-means clustering and 
def dom_color(img_path: str) -> np.array:
    """returns dominant color in an image passed as a path to file as np array"""
    img = io.imread(img_path)[:, :, :-1]
    #img = cv2.imread(img_path, 1)[:, :, :-1]
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    #return (palette)
    return dominant

if __name__ == "__main__":
    d = dom_color("doge.jpg")
    print(d)
    print(dom_color("red.png"))
    