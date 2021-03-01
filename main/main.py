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
from Player import Player


app = Flask(__name__)
app.config["DEBUG"] = True

#globals
cameraMtx = []
distCoeffs = []
projMtx = []

players = []

camera = 0

#Server Routes
@app.route("/", methods=['GET'])
def home():
    return render_template("main.html")

@app.route("/new_player", methods=["POST"])
def new_player():
    name = request.form["name"]
    player_id = len(players)
    player = Player(player_id, name)

    print(player)

    players.append(player)

    print("Players...")
    print(players)

    return redirect(url_for("game", player=json.dumps(player.__dict__)))

@app.route("/game/<player>", methods=["GET", "POST"])
def game(player):
    player = json.loads(player)
    
    try:
        player = players[player["id"]]
    except:
        return redirect("/")

    if request.method == "GET":
        return render_template("game.html", player=player)
    
    if request.method == "POST":
        return jsonify(player.__dict__)

@app.route("/<player_id>/rotate:<rotation>", methods=["POST"])
def rotate(player_id, rotation):
    player_id = int(player_id)
    rotation = int(rotation)
    player = players[player_id]
    player.rotation = rotation
    print("New Rotation for {}: {}".format(player.name, rotation))
    print(players)
    return "OK"


def startup():
    global camera, projMtx, cameraMtx, distCoeffs
    cmd = input("Press enter to start calibration: ")

    cameraMtx, distCoeffs = calibration.calibrateCamera(camera)

    print("Camera calibration complete with the following matrices...")
    print(cameraMtx)
    print(distCoeffs)
    
    input("Press enter to continue...")

    projMtx = calibration.calibrateProjection(camera)

    print("Projection calibrated with the following matrix...")
    print(projMtx)

    input ("Press enter to continue...")

# startup()

def confirm_matrices():
    global projMtx, cameraMtx, distCoeffs
    print("Projection Matrix:")
    print(projMtx)
    print("Camera Matrix:")
    print(cameraMtx)
    print("Distortion Coefficients:")
    print(distCoeffs)

# confirm_matrices()

# marker_recognition.detect(camera, cameraMtx, distCoeffs, projMtx)

# Start a new Thread and run it in the background
# th = threading.Thread(target=marker_recognition.app)
# th.start()
app.run(host="0.0.0.0")
# th.join() 