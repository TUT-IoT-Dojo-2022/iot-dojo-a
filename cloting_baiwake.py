import numpy as np
import matplotlib.pyplot as plt
#k-meansを行うためのプログラム
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
#用いるデータ
data = [10, 10, 18, 16, 14, 13, 19, 16, 14, 16, 12, 14, 12, 26, 22, 20, 20, 26, 24, 24, 12, 3, 16, 16, 7, 10 , 10, 10, 15, 15, 10, 13, 16, 28, 28, 20, 14, 20, 22, 12, 14, 11, 8, 10, 8, 2, 10, 12, 6, 18, 4, 14, 6, 9, 9, 32, 22, 14, 14, 18]
data.sort()
data_lst = []
lst1 = []
lst2 = []
lst3 = []
pittari = 0
nomal = 0
over = 0
L = 0 #ウエストの値
for i, n in enumerate(data,0):
    data_lst_1 = [i, n]
    data_lst.append(data_lst_1)
atumi_data = np.array(data_lst)

#3つのクラスタに分けるモデルを作成
model =  KMeans_pp(3)
model.fit(atumi_data)

#print(model.labels_)

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

#print(pittari)
#print(nomal)
#print(over)

# クラスタリングの画像プロット
markers = ["+", "*", "o", '+']
color = ['r', 'b', 'g', 'k']
for i in range(4):
    p = atumi_data[model.labels_ == i, :]
    plt.scatter(p[:, 0], p[:, 1], marker = markers[i], color = color[i])

plt.show()

clothing_size = int(input("1:ぴちぴちサイズ,2:ちょうどいいサイズ,3:オーバサイズから数字を1つ選んでください."))
if clothing_size == 1:
    L = L - pittari
elif clothing_size == 2:
    L = L - nomal
elif clothing_size == 3:
    L = L - over
print(L)