from asyncio.windows_utils import pipe
import os
import imageio
import convert_to_square as cts


# data preprocessing
def pipeline():
    os.makedirs("../images/source", exist_ok=True)
    os.makedirs("../images/squared", exist_ok=True)
    os.makedirs("../images/final", exist_ok=True)

    files = os.listdir("../images/source")
    i = 0
    for file in files:
        try:
            img = imageio.read_image(f"../images/source/{file}")
        except FileNotFoundError:
            pass
        img = cts.make_square(img, 64)
        
        i+=1

        

if __name__ == "__main__":
    pipeline()
