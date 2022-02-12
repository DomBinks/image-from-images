import cv2
import numpy as np
from skimage import io
from sklearn.cluster import KMeans
import imageio
import convert_to_square as cts

# returns dominant color in an image as RGB values in np array of size 3 [R, G, B]
# input: path to an image file to profile.
# Uses k-means clustering
def dom_color(img_path: str) -> np.array:
    """Returns dominant color RGB array for the image provided"""
    
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))

    #finidng dominant colors
    cluster = KMeans(n_clusters=5).fit(reshape)
    # print(cluster)

    # change index from 0 -> if things being janky
    return cluster.cluster_centers_[0]
    
    #return palette
    

if __name__ == "__main__":
    img = imageio.read_image("../images/source/mike.jpg")
    img = cts.make_square(img, 64)
    imageio.write_image(img, "../images/squared/mike.jpg")
    print(dom_color("../images/squared/mike.jpg"))
    #print(dom_color("../images/source/red.png"))
    