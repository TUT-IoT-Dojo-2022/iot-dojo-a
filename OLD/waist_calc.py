import math

room_yoko = 71 #測定する場所の横幅
room_tate = 71 #測定する場所の奥行
SIZE = 2 #ぴちぴち:1 / ちょうどいい:2 / オーバー：3
CLOTHES_TYPE = 0 #上着なし:0 / 上着あり：1

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
c0 = (r1 - r2) / (r1 + r2)
c1 = math.pi * (r1 + r2)
c2 = 3 * math.pow(c0, 2)
c3 = math.sqrt(4 - 3 * math.pow(c0, 2))
L = c1 * (1 + c2 / (10 + c3))
with open("./files/waist.txt", mode="w") as f:
    f.write(str(L))
