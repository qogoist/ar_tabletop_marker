import cv2
import numpy as np
import imutils
import sys
import threading
import time
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

import marker_recognition
import calibration


app = Flask(__name__)
app.config["DEBUG"] = True

#globals
cameraMtx = []
distCoeffs = []
projMtx = []

players = []

#Server Routes
@app.route("/", methods=['GET'])
def home():
    return render_template("main.html")

@app.route("/new_player", methods=["POST"])
def new_player():
    name = request.form["name"]
    player_id = len(players)
    player_obj = {
        "name": name,
        "id": player_id
    }

    players.append(player_obj)

    print("Players...")
    print(players)

    return redirect(url_for("game", player=json.dumps(player_obj)))

@app.route("/game/<player>", methods=["GET"])
def game(player):
    player = json.loads(player)
    return render_template("game.html", player=player)

def startup():
    global projMtx, cameraMtx, distCoeffs
    cmd = input("Press enter to start calibration: ")

    cameraMtx, distCoeffs = calibration.calibrateCamera()

    print("Camera calibration complete with the following matrices...")
    print(cameraMtx)
    print(distCoeffs)
    
    input("Press enter to continue...")

    projMtx = calibration.calibrateProjection()

    print("Projection calibrated with the following matrix...")
    print(projMtx)

    input ("Press enter to continue...")

startup()

def confirm_matrices():
    global projMtx, cameraMtx, distCoeffs
    print("Projection Matrix:")
    print(projMtx)
    print("Camera Matrix:")
    print(cameraMtx)
    print("Distortion Coefficients:")
    print(distCoeffs)

confirm_matrices()

marker_recognition.detect(cameraMtx, distCoeffs, projMtx)

# Start a new Thread and run it in the background
# th = threading.Thread(target=marker_recognition.app)
# th.start()
# app.run(host="0.0.0.0")
# th.join() 