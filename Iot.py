import numpy as np
from scipy.special import ellipe
#データの処理（円周の代表値を出す）
room_yoko = 71 #測定する場所の横幅
room_tate = 71 #測定する場所の奥行
L1 = 23 #センサーの左側
L2 = 26 #センサーの右側
L3 = 21 #センサーの背中
L4 = 34 #センサーのお腹側
daen_yoko = (room_yoko - (L1 + L2)) / 2
daen_tate = (room_tate - (L4 + L3)) / 2
if daen_yoko >= daen_tate:
    L = 4 * daen_yoko * ellipe(e)
    print("f{:.3F}".format(L))
elif daen_yoko < daen_tate:
    L = 4 * daen_tate * ellipe(e)
    print("f{:.3F}".format(L))
