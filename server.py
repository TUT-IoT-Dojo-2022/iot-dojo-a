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

@app.route("/dist", methods=["POST"])
def main():
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
