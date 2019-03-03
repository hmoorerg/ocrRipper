from flask import Flask,flash,jsonify,redirect,url_for, request, render_template,send_from_directory
app = Flask(__name__)
import base64

app.secret_key = b'_5#yzxcxzcxz2L"F4Q8z\n\xec]/'

from google.cloud import vision

client = vision.ImageAnnotatorClient()


@app.route("/")
def index():
    return send_from_directory("public","index.html")

import json

# @app.route("/<location>")
# def hello(location):
#     location = 'https://help.r2docuo.com/en/lib/R2Docuo_App_Sign_1.png'
#     response = client.annotate_image({
#         'image': {'source': {'image_uri': location}},
#         'features': [{'type': vision.enums.Feature.Type.TEXT_DETECTION}]
#     })

#     found_txt = response.text_annotations
#     return json.dumps(found_txt[4].description)

data = {}

@app.route("/clear")
def clear():
    global data
    # Reset the 'Database'
    data = {}

    return "Done clearing data"

@app.route("/list")
def lst():
    table = render_template('grid.html',data=data)    

    return table

def sort_vertices(vertices_list):
    vertices_list.sort(key = lambda v: v.x)
    

@app.route("/upload",methods=['Post'])
def upload():
    global data
    file = request.files['file']

    config = {
        'image': {"content":file.read()},
        'features': [{'type': vision.enums.Feature.Type.TEXT_DETECTION}]
    }

    flash("Read image")
    response = client.annotate_image(config)

    found_txt = response.text_annotations



    name = ""
    date = ""

    #loop over each found string
    for txt in found_txt:
        vertices = txt.bounding_poly.vertices
        sort_vertices(vertices)
        (start_x,start_y) = (vertices[0].x,vertices[0].y)
        
        
        (end_x,end_y) = (vertices[3].x,vertices[3].y)

        avg_x = (start_x + end_x) / 2
        avg_y = (start_y + end_y] / 2

        # Name
        if start_x > 560 and end_x < 1000:
            if start_y > 700 and end_y < 919:
                print(txt.description)
                name += " "+txt.description
        
        # Date
        if start_x > 370 and end_x < 600:
            if start_y > 700 and end_y < 910:
                if not (txt.description in ['Signature:','(print)',"Name","(orint","(orint)"]):
                    print(txt.description)
                    date += txt.description
        

    data[name] = date
    print("Name:",name)
    print("Date:",date)
        
    return redirect(url_for('lst'))

