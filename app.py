from flask import Flask,flash,jsonify,redirect,url_for, request, render_template,send_from_directory
app = Flask(__name__,static_url_path='')
import base64
from google.cloud import vision
import json

client = vision.ImageAnnotatorClient()


data = {}

@app.route("/")
def index():
    return  send_from_directory("static","index.html")


@app.route("/clear")
def clear():
    global data
    # Reset the 'Database'
    data = {}

    return redirect(url_for('lst'))

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
        avg_y = (start_y + end_y) / 2


        # Name
        if 650 < avg_x < 1000:
            if  700 < avg_y < 919:
                name += " "+txt.description
                # print(avg_x,avg_y,txt.description, sep="\t")
        
        # Date
        if 400 < avg_x < 600:
            if  830 < avg_y < 910:
                date += txt.description
                # print(avg_x,avg_y,txt.description, sep="\t")
        

    data[name] = date
    print("Name:",name)
    print("Date:",date)
        
    return redirect(url_for('lst'))

#app.run()