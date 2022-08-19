from flask import Flask, request, render_template, jsonify
from scipy.special import ellipe
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

#ウエストの値(左側)を取得し，保存
@app.route("/wleft", methods=["POST"])
def waist_left():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  print("Waist Left: " + str(dist_mode) + "cm")
  with open("./waist_left.txt", mode="w") as f:
    f.write(str(dist_mode))

  return jsonify(dist_mode)

#ウエストの値(右側)を取得し，保存
@app.route("/wright", methods=["POST"])
def waist_right():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  print("Waist Right: " + str(dist_mode) + "cm")
  with open("./waist_right.txt", mode="w") as f:
    f.write(str(dist_mode))

  return jsonify(dist_mode)

def waist_circle():
  #データの処理（円周の代表値を出す）
  room_yoko = 71 #測定する場所の横幅
  room_tate = 71 #測定する場所の奥行
  L1 = 23 #センサーの左側
  L2 = 26 #センサーの右側
  L3 = 21 #センサーの背中
  L4 = 34 #センサーのお腹側
  daen_yoko = (room_yoko - (L1 + L2)) / 2
  daen_tate_1 = (room_tate - (L3 + L3)) / 2
  daen_tate_2 = (room_tate - (L4 + L4)) / 2
  L = 4 * daen_yoko * ellipe(e)
  print("f{:.3F}".format(L))

# @app.route("/")
# def shouldwidFront ():#肩幅の計算(正面)
#   res = 0
  
#   return jsonify(res)

# @app.route("/")
# def shouldwidSide ():#肩幅の計算(側面)
#   res = 0
  
#   return jsonify(res)

# @app.route("/")
# def clothesDiffSave():#着衣と素肌の差を測ってファイル保存
#   res = 0
  
#   return jsonify(res)

# @app.route("/")
# def clothDiffCorrect():#着衣と素肌の誤差を補正
#   res = 0
  
#   return jsonify(res)

# @app.route("/")
# def measureCalculat():#誤差の許容範囲の計算
#   res = 0
  
#   return jsonify(res)

# @app.route("/")
# def outValue():#外れ値除外のアルゴリズム
#   res = 0
  
#   return jsonify(res)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
