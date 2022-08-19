from flask import Flask, request, render_template, jsonify
from scipy.special import ellipe
import time
import statistics
import json
import requests

room_height = 175
room_yoko = 71 #測定する場所の横幅
room_tate = 71 #測定する場所の奥行
inseam_fix = 50

app = Flask(__name__)

@app.route("/")
def web_view():
  dist = ""
  try:
    with open("./files/head.txt") as f:
      dist = f.read()
  except:
    with open("./files/head.txt", mode="w") as f:
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
  with open("./files/head.txt", mode="w") as f:
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
  with open("./files/legs.txt", mode="w") as f:
    f.write(str(result_dist))

  return jsonify(result_dist)

#ウエストの値(円周)を計算し，返す
@app.route("/waist", methods=["POST"])
def waist_circle():
  try:
    with open("./files/waist_left.txt") as f:
      L1 = int(f.read())
    with open("./files/waist_right.txt") as f:
      L2 = int(f.read())
    #データの処理（円周の代表値を出す）
    L3 = 21 #センサーの背中
    L4 = 34 #センサーのお腹側
    daen_yoko = (room_yoko - (L1 + L2)) / 2
    daen_tate_1 = (room_tate - (L3 + L3)) / 2
    daen_tate_2 = (room_tate - (L4 + L4)) / 2
    L = 4 * daen_yoko * ellipe(e)
    print("f{:.3F}".format(L))
  except:
    L = None
  return L

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
  with open("./files/waist_left.txt", mode="w") as f:
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
  with open("./files/waist_right.txt", mode="w") as f:
    f.write(str(dist_mode))

  return jsonify(dist_mode)

#肩幅の値(円周)を計算し，返す
@app.route("/shoulder", methods=["POST"])
def shoulder_circle():
  try:
    with open("./files/shoulder_left.txt") as f:
      L1 = int(f.read())
    with open("./files/shoulder_right.txt") as f:
      L2 = int(f.read())
    #データの処理（円周の代表値を出す）
    L3 = 21 #センサーの背中
    L4 = 34 #センサーのお腹側
    daen_yoko = (room_yoko - (L1 + L2)) / 2
    daen_tate_1 = (room_tate - (L3 + L3)) / 2
    daen_tate_2 = (room_tate - (L4 + L4)) / 2
    L = 4 * daen_yoko * ellipe(e)
    print("f{:.3F}".format(L))
  except:
    L = None
  return L

#ウエストの値(左側)を取得し，保存
@app.route("/sleft", methods=["POST"])
def shoulder_left():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  print("Shoulder Left: " + str(dist_mode) + "cm")
  with open("./files/shoulder_left.txt", mode="w") as f:
    f.write(str(dist_mode))

  return jsonify(dist_mode)

#肩幅の値(右側)を取得し，保存
@app.route("/sright", methods=["POST"])
def shoulder_right():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  print("Shoulder Right: " + str(dist_mode) + "cm")
  with open("./files/shoulder_right.txt", mode="w") as f:
    f.write(str(dist_mode))

  return jsonify(dist_mode)

#着衣と素肌の差を測ってファイル保存（上着なし）
@app.route("/clothes1", methods=["POST"])
def clothesDiffSave1():
  data = request.get_json(force=True)
  distance = data['distance']
  with open("./files/clothes1.txt", mode="a") as f:
    f.write(str(distance))
  return jsonify(distance)

#着衣と素肌の差を測ってファイル保存（上着あり）
@app.route("/clothes2", methods=["POST"])
def clothesDiffSave2():
  data = request.get_json(force=True)
  distance = data['distance']
  with open("./files/clothes2.txt", mode="a") as f:
    f.write(str(distance))
  return jsonify(distance)

# @app.route("/")
# def clothDiffCorrect():#着衣と素肌の誤差を補正
#   res = 0
  
#   return jsonify(res)

def outValue():#外れ値除外のアルゴリズム
  res = 0
  return jsonify(res)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
