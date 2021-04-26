#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

V = "fish and chips"
W = "sushi"
X = "churros"
Y = "donuts"
Z = "paella"

sampleV = "static/fish_and_chips.jpg"
sampleW = "static/sushi.jpg"
sampleX = "static/eclairfull.png"
sampleY = "static/eclair.png"
sampleZ = "static/paella.jpg"

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

import os

from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import numpy as np

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.compat.v1.keras.backend import set_session
import tensorflow.compat.v1 as tf

tf.compat.v1.disable_eager_execution()

app = Flask(__name__)

def load_model_from_file():
    
    session = tf.Session()
    set_session(session)
    model = load_model("model.hdf5")#aqui va el modelo cuando acabe
    graph = tf.get_default_graph()
    
    return session, model, graph

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods = ["GET", "POST"])

def upload_file():
    if request.method == "GET":
        return render_template("index.html", myV = V, myW = W, myX = X, 
                               myY = Y, myZ = Z, mySampleV = sampleV,
                               mySampleW = sampleW, mySampleX = sampleX,
                               mySampleY = sampleY, mySampleZ = sampleZ)
    else:
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        
        if file.filename == "":
            flash("No file selected")
        if not allowed_file(file.filename):
            flash("It only accepts files of type" + str(ALLOWED_EXTENSIONS))
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploaded_file", filename = filename))
        
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    test_image = image.load_img(UPLOAD_FOLDER+"/"+filename,target_size=(512,512))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    test_image /= 255.
    
    session = app.config["SESSION"]
    model = app.config["MODEL"]
    graph = app.config["GRAPH"]
    
    with graph.as_default():
        set_session(session)
        result = model.predict(test_image)
        image_src = "/"+UPLOAD_FOLDER+"/"+filename
        result = np.argmax(result)
        if result == 0:
            answer = "<div class='container'><div class='row'><div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4 class='white'>Guess: "+X+"</h4></div><div class='col'></div><div class='w-100'></div></div></div>"
        elif result == 1:
            answer = "<div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4 class='white'>Guess: "+Y+"</h4></div><div class='col'></div><div class='w-100'></div>"
        elif result == 2:
            answer = "<div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4 class='white'>Guess: "+V+"</h4></div><div class='col'></div><div class='w-100'></div>"
        elif result == 3:
            answer = "<div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4 class='white'>Guess: "+Z+"</h4></div><div class='col'></div><div class='w-100'></div>"
        else:
            answer = "<div class='col text-center'><img width='150' height='150' src='"+image_src+"' class='img-thumbnail' /><h4 class='white'>Guess: "+W+"</h4></div><div class='col'></div><div class='w-100'></div>"
        results.append(answer)
        return render_template("index.html", myV = V, myW = W, myX = X, 
                               myY = Y, myZ = Z, mySampleV = sampleV,
                               mySampleW = sampleW, mySampleX = sampleX,
                               mySampleY = sampleY, mySampleZ = sampleZ, 
                               len = len(results), results = results)
def main():
    
    (session, model, graph) = load_model_from_file()
    
    app.config["SECRET_KEY"] = "secret key for first project"
    
    app.config["SESSION"] = session
    app.config["MODEL"] = model
    app.config["GRAPH"] = graph
    
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.run()

    
results = []

main()
