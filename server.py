from dis import dis
import math
import statistics
import numpy as np
from scipy.special import ellipe
from flask import Flask, request, render_template, jsonify

BOX_HEIGHT = 194 #高さ
BOX_YOKO = 109 #測定する場所の横幅
BOX_TATE = 109 #測定する場所の奥行
INSEAM_FIX = 65 #股下の補正値
CLOTHES_FIX = 0 #服の補正値
SIZE = 1 #ぴちぴち:1 / ちょうどいい:2 / オーバー：3
FUNC_NUM = 0 #初期値:0 / 身長・股下の終了時:1 / 肩幅開始時:2 / ウエスト左右開始時:3 / ウエスト前後開始時:4 / 測定終了時:5
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
    shoulder_calc()
    with open("./files/shoulder.txt") as f:
      shoulder = int(f.read())
  except:
    shoulder = " -- "
  try:
    waist_circle()
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
    with open("./files/waist_right.txt") as f:
      waist_a = int(f.read())
    with open("./files/waist_left.txt") as f:
      waist_c = int(f.read())
    with open("./files/waist_back.txt") as f:
      waist_b = int(f.read())
    with open("./files/waist_front.txt") as f:
      waist_d = int(f.read())
  except:
    waist_a = waist_b = waist_c = waist_d = " -- "
  return render_template("index.html", data=[height,shoulder,waist,legs,(BOX_HEIGHT-height),raw_kata_a,raw_kata_b,str(int(legs)-INSEAM_FIX),waist_a,waist_b,waist_c,waist_d,int(CLOTHES_FIX)])

# 以下、服のSIZE及びFUNC_NUMの受取
@app.route('/home')
def clothes_form():
  return render_template('get_clothes.html')

# 服の大きさをpost取得 & get_heightの描画
@app.route('/get_clothes', methods=['post'])
def getClothes():
  global SIZE
  global FUNC_NUM
  SIZE = int(request.form['get_clothes']) # FUNC_NUM = 1 | 2 | 3
  FUNC_NUM = 0
  print("SIZE : " + str(SIZE))
  return render_template('get_height.html')

# 身長のFUNC_NUMをpost取得 & get_kataの描画
@app.route('/get_height', methods=['post'])
def getHeight():
  global FUNC_NUM
  FUNC_NUM = int(request.form['get_height']) # FUNC_NUM = 1
  print("FUNC_NUM : " + str(FUNC_NUM))
  return render_template('get_kata.html')

# 肩のFUNC_NUMをpost取得 & get_waist_sideの描画
@app.route('/get_kata', methods=['post'])
def getKata():
  global FUNC_NUM
  FUNC_NUM = int(request.form['get_kata']) # FUNC_NUM = 2
  print("FUNC_NUM : " + str(FUNC_NUM))
  return render_template('get_waist_side.html')

# ウエスト側面のFUNC_NUMをpost取得 & get_waist_frontの描画
@app.route('/get_waist_side', methods=['post'])
def getWaistSide():
  global FUNC_NUM
  FUNC_NUM = int(request.form['get_waist_side']) # FUNC_NUM = 3
  print("FUNC_NUM : " + str(FUNC_NUM))
  return render_template('get_waist_front.html')

# ウエスト前面のFUNC_NUMをpost取得 & get_endの描画
@app.route('/get_waist_front', methods=['post'])
def getWaistFront():
  global FUNC_NUM
  FUNC_NUM = int(request.form['get_waist_front']) # FUNC_NUM = 4
  print("FUNC_NUM : " + str(FUNC_NUM))
  return render_template('get_end.html')
    
# 終了値のFUNC_NUMをpost取得
@app.route('/get_end', methods=['post'])
def getEnd():
  global FUNC_NUM
  FUNC_NUM = int(request.form['get_end']) # FUNC_NUM = 5 終了
  print("FUNC_NUM : " + str(FUNC_NUM))
  return web_view()

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
  result_dist = BOX_HEIGHT - dist_mode
  if FUNC_NUM < 1:
    print("Height: " + str(dist_mode) + "cm(" + str(result_dist) + ")")
    with open("./files/height.txt", mode="w") as f:
      f.write(str(result_dist))
  else:
    print("Height Skip")
  return jsonify()

#距離センサーの値を取得し，股下の計算（legs.txtで保存)
@app.route("/legs", methods=["POST"])
def inseam_mode():
  global INSEAM_FIX
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  if dist_mode < 10:
    INSEAM_FIX = 70
  elif dist_mode >= 90:
    INSEAM_FIX = 0
  else:
    INSEAM_FIX = int((75 - dist_mode) / 10) * 10
  result_dist = dist_mode + INSEAM_FIX
  if FUNC_NUM < 1:
    print("Inseam: " + str(dist_mode) + "cm(" + str(result_dist) + ")")
    with open("./files/legs.txt", mode="w") as f:
      f.write(str(result_dist))
  else:
    print("Inseam Skip")
  return jsonify(result_dist)

#側面（左）の距離センサーの値を取得し，関数呼び出し
@app.route("/left", methods=["POST"])
def dist_left_mode():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  if FUNC_NUM == 2:
    with open("./files/shoulder_left.txt", mode="w") as f:
      f.write(str(dist_mode))
  elif FUNC_NUM == 3:
    with open("./files/waist_left.txt", mode="w") as f:
      f.write(str(dist_mode))
  elif FUNC_NUM == 4:
    waist_front(dist_mode)
  else:
    with open("./files/left.txt", mode="w") as f:
      f.write(str(dist_mode))
  print("Left: " + str(dist_mode) + "cm")
  return jsonify(FUNC_NUM, dist_mode)

#側面（右）の距離センサーの値を取得し，関数呼び出し
@app.route("/right", methods=["POST"])
def dist_right_mode():
  data = request.get_json(force=True)
  distance = data['distance']
  dist_db = []
  for d in distance:
    dist_cm = int(round(d) / 10.0) 
    dist_db.append(dist_cm)
  dist_mode = statistics.mode(dist_db)
  if FUNC_NUM == 2:
    with open("./files/shoulder_right.txt", mode="w") as f:
      f.write(str(dist_mode))
  elif FUNC_NUM == 3:
    with open("./files/waist_right.txt", mode="w") as f:
      f.write(str(dist_mode))
  elif FUNC_NUM == 4:
    waist_back(dist_mode)
  else:
    with open("./files/right.txt", mode="w") as f:
      f.write(str(dist_mode))
  print("Right: " + str(dist_mode) + "cm")
  return jsonify(FUNC_NUM, dist_mode)

def shoulder_calc():
  with open("./files/shoulder_left.txt") as f:
    s_l = int(f.read())
  with open("./files/shoulder_right.txt") as f:
    s_r = int(f.read())
  sld = BOX_YOKO - (s_l + s_r)
  with open("./files/shoulder.txt", mode="w") as f:
      f.write(str(sld))

#ウエストの値(円周)を計算し，返す
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
    r1 = (BOX_YOKO - (L1 + L2)) / 2 #長径
    r2 = (BOX_TATE - (L3 + L4)) / 2 #短径
    if r1 >= r2:
      e = np.sqrt(r1 ** 2 - r2 ** 2) / r1
      L = 4 * r1 * ellipe(e)
    elif r2 > r1:
      e = np.sqrt(r2 ** 2 - r1 ** 2) / r2
      L = 4 * r2 * ellipe(e)
    with open("./files/waist.txt", mode="w") as f:
      f.write(str(round(L)))
  except:
    L = None
  return L

#ウエストの値を計算し，保存
def waist_front(dist):
  dist_mode = dist
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
  return jsonify(L)

#ウエストの値を取得し，保存
def waist_back(dist):
  dist_mode = dist
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
  return jsonify(L)

#着衣と素肌の誤差を補正
def clothDiffCorrect(L):
  global CLOTHES_FIX
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

#もし動かないとき消去する
  with open ("./files/k-means.txt") as f:
    for i in f:
      i = int(i)
      data.append(i)
  #テキストファイルが読み込まれず、動かない場合
  #data = [10, 10, 18, 16, 14, 13, 19, 16, 14, 16, 12, 14, 12, 26, 22, 20, 20, 26, 24, 24, 12, 3, 16, 16, 7, 10 , 10, 10, 15, 15, 10, 13, 16, 28, 28, 20, 14, 20, 22, 12, 14, 11, 8, 10, 8, 2, 10, 12, 6, 18, 4, 14, 6, 9, 9, 32, 22, 14, 14, 18]
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
      CLOTHES_FIX = pittari
      L = L + pittari
  elif SIZE == 2:
      CLOTHES_FIX = nomal
      L = L + nomal
  elif SIZE == 3:
      CLOTHES_FIX = over
      L = L + over
  return L

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