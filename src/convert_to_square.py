from re import S
import cv2


if __name__ == "__main__":
    image = cv2.imread('../images/mike.jpg', 1)
    height, width = image.shape[:2]
    print("Height:%s width:%s" % (height, width))

    if height < width:
        l_offset = height // 2
        r_offset = height // 2

        if height % 2 != 0:
            r_offset = int(height / 2) + 1

        image = image[0:height, int((int(width / 2) - l_offset)):int((int(width / 2) + r_offset))]
        
    cv2.imwrite('../images/squared/mike.jpg', image)

    cv2.imshow('img',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()