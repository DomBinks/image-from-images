import os

from matplotlib import image
import imageio
import convert_to_square as cts
import pandas as pd
import tint
import get_dominant_color as gdc
import convert_to_16 as ct16
import shutil
import stitching

def cleanup():
    try:
        shutil.rmtree("../images/squared")
        shutil.rmtree("../images/tinted")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

# data preprocessing
def pipeline(colors):
    os.makedirs("../images/source", exist_ok=True)
    os.makedirs("../images/squared", exist_ok=True)
    os.makedirs("../images/final", exist_ok=True)
    os.makedirs("../images/reduced", exist_ok=True)

    color_keys = colors['key'].to_list()
    
    for color in color_keys:
        os.makedirs(f"../images/tinted/{color}", exist_ok=True)

    # Squaring
    files = os.listdir("../images/source")
    i = 0
    for file in files:
        try:
            img = imageio.read_image(f"../images/source/{file}")
            img = cts.make_square(img, 64)
            file = file.lower()
            if "jpg" in file[-3:] or "jpeg" in file[-4:]:
                ext = "jpg"
            elif "png" in file[-3:]:
                ext = "png"
            else:
                raise ValueError
            imageio.write_image(img, f"../images/squared/{i}.{ext}")
            i+=1
        except FileNotFoundError:
            pass
        except ValueError:
            pass
    
    # Tinting
    files = os.listdir("../images/squared")
    for file in files:
        try:
            file = file.lower()
            if "jpg" in file[-3:] or "jpeg" in file[-4:]:
                ext = "jpg"
            elif "png" in file[-3:]:
                ext = "png"
            else:
                raise ValueError
            path =f"../images/squared/{file}"
            
            dom_color = gdc.dom_color(path)
            tint_color = ct16.rgb_to_nearest_16(dom_color, colors)
            img = imageio.read_image(path)
            img = tint.tint(img, tint_color['r'], tint_color['g'], tint_color['b'])

            imageio.write_image(img, f"../images/tinted/{tint_color['key']}/{file}")
        except FileNotFoundError:
            pass
        except ValueError:
            pass

def select_input_file():
    files = os.listdir("../images/input")
    
    print("Please select a file from the list below as input:")
    for i in range(len(files)):
        print(f"    [{i}] {files[i]}")
    file_no = int(input("File number: "))
    while file_no < 0 or file_no >= len(files):
        print("Invalid response please enter a valid file number")
        file_no = int(input("File number: "))
    
    return files[file_no]

def reduce_to_16(file, df_colors):
    # need to optimise
    img = imageio.read_image(f"../images/input/{file}")
    img = cts.make_square(img, 64)
    img = ct16.make_16(img, df_colors)
    imageio.write_image(img, f"../images/reduced/{file}")
    return img
    
#pog
if __name__ == "__main__":
    # can do async
    input_file = select_input_file()
    df_colors = pd.read_csv("../colors.csv")
    cleanup()
    pipeline(df_colors)
    img = reduce_to_16(input_file, df_colors)
    stitching.stitch(img, df_colors, grid_size=64)
    

