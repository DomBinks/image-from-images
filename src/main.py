import os
import imageio
import convert_to_square as cts


# data preprocessing
def pipeline():
    os.makedirs("../images/source", exist_ok=True)
    os.makedirs("../images/squared", exist_ok=True)
    os.makedirs("../images/final", exist_ok=True)


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
        

if __name__ == "__main__":
    pipeline()
