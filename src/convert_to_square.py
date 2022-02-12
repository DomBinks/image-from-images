from re import S
import cv2


if __name__ == "__main__":
    image = cv2.imread('../images/mike.jpg', 1)
    height, width = image.shape[:2]
    print("Height:%s width:%s" % (height, width))
    
    #image = image[0:height, (int(width / 2) - int(height / 2)):(int(width / 2) + int(height / 2))]
    image = image[0:height, 0:width]

    if height > width:
        if height % 2 == 0:
            l_offset = height / 2
            r_offset = height / 2
        else:
            l_offset = int(height / 2)
            r_offset = int(height / 2) + 1

            image = image[0:height, (width / 2 - height / 2):(width / 2 + height / 2)]
        

    cv2.imshow('img',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 