from flask import Flask, request, render_template, jsonify
import time
import statistics
import json
import requests

app = Flask(__name__)

@app.route("/")
def web_view():
  dist = ""
  with open("./head.txt") as f:
    dist = f.read()
  return render_template("index.html", data=dist)

@app.route("/height", methods=["POST"])
def height_mode():
  data = request.get_json(force=True)
  distance = data['distance']
  name = data['device']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  room_height = 204
  if name == "head":
    result_dist = room_height - dist_mode
    print("Height: " + str(dist_mode) + "cm(" + str(result_dist) + ")")
    with open("./head.txt", mode="w") as f:
      f.write(str(result_dist))
  elif name == "side":
    print("Side:", result_dist)
  return jsonify(dist_mode)

### 寺内くんお願い



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route("/")
def distanceSave():
  res = 0
  
  return jsonify(res)

@app.route("/")
def clothesDiffSave():
  res = 0
  
  return jsonify(res)

@app.route("/")
def inseam():
  res = 0
  
  return jsonify(res)

@app.route("/")
def shouldwidFront ():
  res = 0
  
  return jsonify(res)

@app.route("/")
def shouldwidSide ():
  res = 0
  
  return jsonify(res)
  
@app.route("/")
def westFront ():
  res = 0
  
  return jsonify(res)

@app.route("/")
def westSide ():
  res = 0
  
  return jsonify(res)

@app.route("/")
def clothDiffCorrect():
  res = 0
  
  return jsonify(res)

@app.route("/")
def measureCalculat():
  res = 0
  
  return jsonify(res)

@app.route("/")
def outValue():
  res = 0
  
  return jsonify(res)
