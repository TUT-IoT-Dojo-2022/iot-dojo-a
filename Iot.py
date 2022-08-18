
import numpy as np
from scipy.special import ellipe
#データの処理（円周の代表値を出す）
room_yoko = 0 #測定する場所の横幅
room_tate = 0 #測定する場所の奥行
L1 = 0 #センサーの左側
L2 = 0 #センサーの右側
L3 = 0 #センサーの背中
L4 = 0 #センサーのお腹側

daen_yoko = room_yoko - (L1 + L2)
daen_tate = room_tate - (L3 + L4)
if daen_yoko >= daen_tate:
    e = np.sqrt(daen_yoko**2 - daen_tate**2) / daen_yoko
    L = 4 * daen_yoko  * ellipe(e)
    print("f{:.3F}".format(L))
else:
    e = np.sqrt(daen_tate**2 - daen_yoko**2) / daen_tate
    L = 4 * daen_tate  * ellipe(e)
    print("f{:.3F}".format(L))
