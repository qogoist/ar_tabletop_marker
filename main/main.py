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
    calib_image = cv2.imread("main/local/pattern_chessboard.png")
    win = "Calibration"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    cv2.imshow(win, calib_image)

    print("Showing calibration pattern, please adjust it so it is visible on the projector.")
    cmd = input("Press enter to continue with calibration: ")

    cameraMtx, distCoeffs = calibration.calibrate()
    print(cameraMtx)
    print(distCoeffs)
    
    cv2.waitKey()

startup()

# Start a new Thread and run it in the background
# th = threading.Thread(target=marker_recognition.app)
# th.start()
# app.run(host="0.0.0.0")
# th.join() 