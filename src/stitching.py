from PIL import Image

def create_canvas(size_of_pixel=64, grid_width=256, grid_height=256):
    width  = size_of_pixel * grid_width
    height = size_of_pixel * grid_height
    canvas = Image.new("RGB", [width, height], (255,255,255))
    return canvas

if __name__ == "__main__":
    # create new canvas image

    create_canvas().save("test.jpg")
    pass
