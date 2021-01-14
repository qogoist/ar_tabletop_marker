import sys
import threading
import time
from flask import Flask, render_template

import cont_rec

app = Flask(__name__)
app.config["DEBUG"] = True

counter = 0


@app.route('/', methods=['GET'])
def home():
    return render_template("main.html")


@app.route("/add", methods=["GET"])
def add():
    global counter
    counter += 1

    return str(counter)

th = threading.Thread(target=cont_rec.contour_recognition)

th.start()

app.run()

th.join()