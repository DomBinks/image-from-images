import cv2
import numpy as np
from skimage import io
import imageio
import convert_to_square as cts

# returns dominant color in an image as RGB values in np array of size 3 [R, G, B]
# input: path to an image file to profile.
# Uses k-means clustering
def dom_color(img_path: str) -> np.array:
    """Returns dominant color RGB array for the image provided"""
    img = io.imread(img_path)[:, :, :-1]
    try:
        pixels = np.float32(img.reshape(-1, 3))
    except ValueError:
        pixels = np.float32(img.reshape(-1, 3))
    #pixels = np.float32(img)
    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    return dominant
    #return palette

if __name__ == "__main__":
    img = imageio.read_image("../images/source/red.png")
    img = cts.make_square(img, 99)
    imageio.write_image(img, "../images/squared/red.png")
    print(dom_color("../images/squared/red.png"))
    print(dom_color("../images/source/red.png"))
    