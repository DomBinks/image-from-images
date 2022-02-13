from importlib.resources import contents
import os

from matplotlib import image
import imageio
from mercantile import children
from pandas_datareader import test
import convert_to_square as cts
import pandas as pd
import tint
import get_dominant_color as gdc
import convert_to_16 as ct16
import shutil
import stitching
from dash import Dash, html
from dash import dcc
from dash.dependencies import Input, Output, State
import base64
import flask

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
    os.makedirs("../images/input", exist_ok=True)
    os.makedirs("../images/output", exist_ok=True)

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


app = Dash(__name__)

app.layout = html.Div([
    html.H3(children =  "image from images"),
    html.P(children="Please upload an image to be imaged: "),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.P(children="Output (will take 1 minute):"),
    #html.Img(src="/output.png"),
    html.Div(id="output-image"),

])

def save_file(name, content):
    print(name)
    data = content.encode("utf8").split(b";base64,")[1]
    with open(f"../images/input/{name}", "wb") as fp:
        fp.write(base64.decodebytes(data))
        print("test")


@app.server.route("/output.png")
def serve_static(resource):
    return flask.send_file("../images/output/output.png", mimetype="image/png")


@app.callback(Output("output-image", "children"),
              #Output("output-image", 'src'),
              Input("upload-image", "contents"),
              State("upload-image", "filename")
)
def parse_upload(contents, filename):
    image_return = html.Div([])

    if filename != None:
        save_file(filename, contents)
        input_file = filename
        main(input_file)

        image_return = html.Div()
        
        encoded_image = base64.b64encode(open(f"../images/output/output.png", 'rb').read())
        image_return = html.Div([
            html.Img(src=f"data:image/png;base64,{encoded_image.decode()}",
                    style={'height': "512px", "width": "512px"})
        ])
        print("Done")


    return image_return

def main(input_file: str):
    df_colors = pd.read_csv("../colors.csv")
    cleanup()
    print("Pre-processing")
    pipeline(df_colors)
    print("Reducing")
    img = reduce_to_16(input_file, df_colors)
    print("Stitching")
    stitching.stitch(img, df_colors, grid_size=64)
#pog
if __name__ == "__main__":
    # can do async
    app.run_server(debug=True)
    
    
    
    

