import math
from flask import Flask, request, render_template, jsonify
from scipy import special
import statistics
import numpy as np
import matplotlib.pyplot as plt

room_height = 194
room_yoko = 110 #測定する場所の横幅
room_tate = 110 #測定する場所の奥行
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
  try:
    with open("./files/shoulder_left.txt") as f:
      raw_kata_a = int(float(f.read()))
  except:
    raw_kata_a = " -- "
  try:
    with open("./files/shoulder_right.txt") as f:
      raw_kata_b = int(float(f.read()))
  except:
    raw_kata_b = " -- "
  try:
    with open("./files/waist.txt") as f:
      waist_a = waist_b = waist_c = waist_d  = int(float(f.read()))
  except:
    waist_a = waist_b = waist_c = waist_d = " -- "
  return render_template("measuring.html", data=[height,shoulder,waist,legs,height,raw_kata_a,raw_kata_b,str(int(legs)-inseam_fix),waist_a,waist_b,waist_c,waist_d])

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
  data = []
  data_lst = []
  lst1 = []
  lst2 = []
  lst3 = []
  pittari = 0
  nomal = 0
  over = 0
  class KMeans_pp:
    def __init__(self, n_clusters, max_iter = 1000, random_seed = 0):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = np.random.RandomState(random_seed)

    def fit(self, X):
        #ランダムに最初のクラスタ点を決定
        tmp = np.random.choice(np.array(range(X.shape[0])))
        first_cluster = X[tmp]
        first_cluster = first_cluster[np.newaxis,:]

        #最初のクラスタ点とそれ以外のデータ点との距離の2乗を計算し、それぞれをその総和で割る
        p = ((X - first_cluster)**2).sum(axis = 1) / ((X - first_cluster)**2).sum()

        r =  np.random.choice(np.array(range(X.shape[0])), size = 1, replace = False, p = p)

        first_cluster = np.r_[first_cluster ,X[r]]

        #分割するクラスター数が3個以上の場合
        if self.n_clusters >= 3:
            #指定の数のクラスタ点を指定できるまで繰り返し
            while first_cluster.shape[0] < self.n_clusters:
                #各クラスター点と各データポイントとの距離の2乗を算出
                dist_f = ((X[:, :, np.newaxis] - first_cluster.T[np.newaxis, :, :])**2).sum(axis = 1)
                #最も距離の近いクラスター点はどれか導出
                f_argmin = dist_f.argmin(axis = 1)
                #最も距離の近いクラスター点と各データポイントとの距離の2乗を導出
                for i in range(dist_f.shape[1]):
                    dist_f.T[i][f_argmin != i] = 0

                #新しいクラスタ点を確率的に導出
                pp = dist_f.sum(axis = 1) / dist_f.sum()
                rr = np.random.choice(np.array(range(X.shape[0])), size = 1, replace = False, p = pp)
                #新しいクラスター点を初期値として加える
                first_cluster = np.r_[first_cluster ,X[rr]]        

        #最初のラベルづけを行う
        dist = (((X[:, :, np.newaxis] - first_cluster.T[np.newaxis, :, :]) ** 2).sum(axis = 1))
        self.labels_ = dist.argmin(axis = 1)
        labels_prev = np.zeros(X.shape[0])
        count = 0
        self.cluster_centers_ = np.zeros((self.n_clusters, X.shape[1]))

        #各データポイントが属しているクラスターが変化しなくなった、又は一定回数の繰り返しを越した場合は終了
        while (not (self.labels_ == labels_prev).all() and count < self.max_iter):
            #その時点での各クラスターの重心を計算する
            for i in range(self.n_clusters):
                XX = X[self.labels_ == i, :]
                self.cluster_centers_[i, :] = XX.mean(axis = 0)
            #各データポイントと各クラスターの重心間の距離を総当たりで計算する
            dist = ((X[:, :, np.newaxis] - self.cluster_centers_.T[np.newaxis, :, :]) ** 2).sum(axis = 1)
            #1つ前のクラスターラベルを覚えておく。1つ前のラベルとラベルが変化しなければプログラムは終了する。
            labels_prev = self.labels_
            #再計算した結果、最も距離の近いクラスターのラベルを割り振る
            self.labels_ = dist.argmin(axis = 1)
            count += 1
            self.count = count

    def predict(self, X):
        dist = ((X[:, :, np.newaxis] - self.cluster_centers_.T[np.newaxis, :, :]) ** 2).sum(axis = 1)
        labels = dist.argmin(axis = 1)
        return labels

  with open ("./files/k-means.txt") as f:
      for i in f:
          i = int(i)
          data.append(i)
  data.sort()
  for i, n in enumerate(data,0):
      data_lst_1 = [i, n]
      data_lst.append(data_lst_1)
  atumi_data = np.array(data_lst)
  #3つのクラスタに分けるモデルを作成
  model =  KMeans_pp(3)
  model.fit(atumi_data)

  #ラベルごとに平均を出す
  for i in range(len(data)):
    if model.labels_[i] == 2:
      lst1.append(data[i])
    elif model.labels_[i] == 1:
      lst2.append(data[i])
    elif model.labels_[i] == 0:
      lst3.append(data[i]) 

  lst1_ave = sum(lst1) / len(lst1)
  lst2_ave = sum(lst2) / len(lst2)
  lst3_ave = sum(lst3) / len(lst3)

  ave_lst = [lst1_ave, lst2_ave, lst3_ave]#平均のリスト作成
  ave_lst.sort()

  #クラスタリングの引く値の抽出
  pittari = round(ave_lst[0])
  nomal = round(ave_lst[1])
  over = round(ave_lst[2])
  if SIZE == 1:
      L = L - pittari
  elif SIZE == 2:
      L = L - nomal
  elif SIZE == 3:
      L = L - over
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
      f.write(str(L - 80))
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