from PIL import Image
from matplotlib.pyplot import grid
import imageio
import random
import os

def create_canvas(size_of_pixel=64, grid_width=256, grid_height=256):
    width  = size_of_pixel * grid_width
    height = size_of_pixel * grid_height
    canvas = Image.new("RGB", [width, height], (255,255,255))
    return canvas


def get_color_key(df_colors, pixel):
    colors_r = df_colors['r'].to_list()
    colors_g = df_colors['g'].to_list()
    colors_b = df_colors['b'].to_list()
    for i in range(len(colors_b)):
        if colors_r[i] == pixel[0] and colors_g[i] == pixel[1] and colors_b[i] == pixel[2]:
            color_row = df_colors.iloc[i]
            return color_row['key']
    return "mg"

def get_random_image(key):
    files = os.listdir(f"../images/tinted/{key}")
    return random.choice(files)

def stitch(input_file, df_colors, pixel_size=64, grid_size=256):
    canvas = create_canvas(grid_height=grid_size, grid_width=grid_size)
    
    height, width = input_file.shape[:2]
    
    for row_index in range(height):
        for col_index in range(width):
            key = get_color_key(df_colors, input_file[row_index][col_index])
            pixel_image_name = get_random_image(key)
            pixel_image = Image.open(f"../images/tinted/{key}/{pixel_image_name}")
            canvas.paste(pixel_image, [col_index*pixel_size, row_index*pixel_size])
            
    canvas.save(f"../images/output/output.jpg")


if __name__ == "__main__":
    # create new canvas image

    create_canvas().save("test.jpg")
    pass
