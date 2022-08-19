from flask import Flask, request, render_template, jsonify
import time
import statistics
import json
import requests

room_height = 175
inseam_fix = 50

app = Flask(__name__)

@app.route("/")
def web_view():
  dist = ""
  try:
    with open("./head.txt") as f:
      dist = f.read()
  except:
    with open("./head.txt", mode="w") as f:
      dist = str(0)
      f.write(dist)
  return render_template("index.html", data=dist)

#距離センサーの値を取得し，身長の計算（head.txtで保存)
@app.route("/head", methods=["POST"])
def height_mode():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  result_dist = room_height - dist_mode
  print("Height: " + str(dist_mode) + "cm(" + str(result_dist) + ")")
  with open("./head.txt", mode="w") as f:
    f.write(str(result_dist))

  return jsonify(result_dist)

#距離センサーの値を取得し，股下の計算（legs.txtで保存)
@app.route("/legs", methods=["POST"])
def inseam_mode():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  result_dist = dist_mode + inseam_fix
  print("Inseam: " + str(dist_mode) + "cm(" + str(result_dist) + ")")
  with open("./legs.txt", mode="w") as f:
    f.write(str(result_dist))

  return jsonify(result_dist)

@app.route("/")
def clothesDiffSave():#着衣と素肌の差を測ってファイル保存
  res = 0
  
  return jsonify(res)

@app.route("/")
def shouldwidFront ():#肩幅の計算(正面)
  res = 0
  
  return jsonify(res)

@app.route("/")
def shouldwidSide ():#肩幅の計算(側面)
  res = 0
  
  return jsonify(res)
  
@app.route("/")
def westFront ():#ウエストの計算(正面)
  res = 0
  
  return jsonify(res)

@app.route("/")
def westSide ():#ウエストの計算(側面)
  res = 0
  
  return jsonify(res)

@app.route("/")
def clothDiffCorrect():#着衣と素肌の誤差を補正
  res = 0
  
  return jsonify(res)

@app.route("/")
def measureCalculat():#誤差の許容範囲の計算
  res = 0
  
  return jsonify(res)

@app.route("/")
def outValue():#外れ値除外のアルゴリズム
  res = 0
  
  return jsonify(res)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
