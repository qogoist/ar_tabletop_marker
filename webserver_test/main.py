import flask
import contour_rec as cr

app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("main.html")

@app.route("/run")
def run():
    pass

if __name__ == "__main__":
    app.run(debug = True)