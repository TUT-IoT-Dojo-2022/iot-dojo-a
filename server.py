import math
from flask import Flask, request, render_template, jsonify
from scipy import special
import statistics

room_height = 203
room_yoko = 71 #測定する場所の横幅
room_tate = 71 #測定する場所の奥行
inseam_fix = 50
SIZE = 2 #ぴちぴち:1 / ちょうどいい:2 / オーバー：3
CLOTHES_TYPE = 0 #上着なし:0 / 上着あり：1

app = Flask(__name__)

@app.route("/")
def web_view():
  try:
    with open("./files/height.txt") as f:
      height = int(f.read())
  except:
    height = " -- "
  try:
    with open("./files/legs.txt") as f:
      legs = int(f.read())
  except:
    legs = " -- "
  try:
    with open("./files/shoulder.txt") as f:
      shoulder = int(f.read())
  except:
    shoulder = " -- "
  try:
    with open("./files/waist.txt") as f:
      waist = int(float(f.read()))
  except:
    waist = " -- "
  return render_template("human.html", data=[height,legs,shoulder,waist])

#距離センサーの値を取得し，身長の計算（height.txtで保存)
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
  with open("./files/height.txt", mode="w") as f:
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

#着衣と素肌の誤差を補正
def clothDiffCorrect(L):
  filename = "./files/clh"
  if CLOTHES_TYPE == 0:
    filename += "1_"
  else:
    filename += "2_"
  if SIZE == 1:
    filename += "pittari.txt"
  elif SIZE == 2:
    filename += "hodoyoi.txt"
  else:
    filename += "over.txt"
  size_data = []
  with open(filename) as f:
    list_line = f.readlines()
    for l in list_line:
      if l[:-1] == "\n":
        l = int(l[:-1])
      else:
        l = int(l)
      size_data.append(l)
  size_avg = sum(size_data) / len(size_data)
  L = L - size_avg
  return L

#ウエストの値(円周)を計算し，返す
#@app.route("/waist", methods=["POST"])
def waist_circle():
  try:
    with open("./files/waist_left.txt") as f:
      L1 = int(f.read())
    L1 = clothDiffCorrect(L1)
    with open("./files/waist_right.txt") as f:
      L2 = int(f.read())
    L2 = clothDiffCorrect(L2)
    with open("./files/waist_front.txt") as f:
      L3 = int(f.read())
    L3 = clothDiffCorrect(L3)
    with open("./files/waist_back.txt") as f:
      L4 = int(f.read())
    L4 = clothDiffCorrect(L4)
    #データの処理（円周の代表値を出す）
    r1 = (room_yoko - (L1 + L2)) / 2 #長径
    r2 = (room_tate - (L3 + L4)) / 2 #短径
    L = (math.pi * (r1 + r2)) * (1 + (3 * math.pow((r1 - r2) / (r1 + r2), 2)) / (10 + math.sqrt(4 - 3 * math.pow((r1 - r2) / (r1 + r2), 2))))
    with open("./files/waist.txt", mode="w") as f:
      f.write(str(L))
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
  try:
    with open("./files/waist_right.txt") as f:
      L2 = int(f.read())
    with open("./files/waist_front.txt") as f:
      L3 = int(f.read())
    with open("./files/waist_back.txt") as f:
      L4 = int(f.read())
    L = waist_circle()
  except:
    L = 0
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
  try:
    with open("./files/waist_left.txt") as f:
      L1 = int(f.read())
    with open("./files/waist_front.txt") as f:
      L3 = int(f.read())
    with open("./files/waist_back.txt") as f:
      L4 = int(f.read())
    L = waist_circle()
  except:
    L = 0
  return jsonify(dist_mode)

#ウエストの値(前側)を取得し，保存
@app.route("/wfront", methods=["POST"])
def waist_front():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  print("Waist Front: " + str(dist_mode) + "cm")
  with open("./files/waist_front.txt", mode="w") as f:
    f.write(str(dist_mode))
  try:
    with open("./files/waist_left.txt") as f:
      L1 = int(f.read())
    with open("./files/waist_right.txt") as f:
      L2 = int(f.read())
    with open("./files/waist_back.txt") as f:
      L4 = int(f.read())
    L = waist_circle()
  except:
    L = 0
  return jsonify(dist_mode)

#ウエストの値(前側)を取得し，保存
@app.route("/wback", methods=["POST"])
def waist_back():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  print("Waist Back: " + str(dist_mode) + "cm")
  with open("./files/waist_back.txt", mode="w") as f:
    f.write(str(dist_mode))
  try:
    with open("./files/waist_left.txt") as f:
      L1 = int(f.read())
    with open("./files/waist_right.txt") as f:
      L2 = int(f.read())
    with open("./files/waist_front.txt") as f:
      L3 = int(f.read())
    L = waist_circle()
  except:
    L = 0
  return jsonify(dist_mode)

#肩幅の値を計算し，返す
#@app.route("/shoulder", methods=["POST"])
def shoulder_circle():
  try:
    with open("./files/shoulder_left.txt") as f:
      L1 = int(f.read())
    with open("./files/shoulder_right.txt") as f:
      L2 = int(f.read())
    yoko = room_yoko - (L1 + L2)
    print(str(yoko) + "cm")
    with open("./files/shoulder.txt", mode="w") as f:
      f.write(str(yoko))
  except:
    yoko = None
  return yoko

#肩幅の値(左側)を取得し，保存
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
  try:
    with open("./files/shoulder_left.txt") as f:
      L1 = int(f.read())
    with open("./files/shoulder_right.txt") as f:
      L2 = int(f.read())
    L = shoulder_circle()
  except:
    L = 0
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
  try:
    with open("./files/shoulder_left.txt") as f:
      L1 = int(f.read())
    with open("./files/shoulder_right.txt") as f:
      L2 = int(f.read())
    L = shoulder_circle()
  except:
    L = 0
  return jsonify(dist_mode)

#着衣と素肌の差を測ってファイル保存（上着なし）
@app.route("/clothes1", methods=["POST"])
def clothesDiffSave1():
  data = request.get_json(force=True)
  distance = int(data['distance'])
  with open("./files/clothes1.txt", mode="a") as f:
    f.write(str(distance)+"\n")
  out_filename = ""
  if 20 < distance:
    out_filename = "./files/clh1_over.txt"
  elif 10 < distance:
    out_filename = "./files/clh1_hodoyoi.txt"
  else:
    out_filename = "./files/clh1_pittari.txt"
  with open(out_filename, mode='a') as f:
    f.writelines(str(distance)+"\n")
  return jsonify(distance)

#着衣と素肌の差を測ってファイル保存（上着あり）
@app.route("/clothes2", methods=["POST"])
def clothesDiffSave2():
  data = request.get_json(force=True)
  distance = data['distance']
  with open("./files/clothes2.txt", mode="a") as f:
    f.write(str(distance)+"\n")
    out_filename = ""
  if 20 < distance:
    out_filename = "./files/clh2_over.txt"
  elif 10 < distance:
    out_filename = "./files/clh2_hodoyoi.txt"
  else:
    out_filename = "./files/clh2_pittari.txt"
  with open(out_filename, mode='a') as f:
    f.writelines(str(distance)+"\n")
  return jsonify(distance)

def outValue():#外れ値除外のアルゴリズム
  res = 0
  return jsonify(res)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
  waist_circle()
