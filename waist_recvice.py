yoyu_atumi = 20 #よゆうのある服の厚み平均
hutu_atumi = 10 #ふつうくらい(?)の服の厚み平均
pita_atumi = 5 #ぴったりの場合の服の厚み
sokutei = 40 #センサーの値から計算したウエストの横幅

def main():
    n = int(input("余裕=1,ふつう=2,ぴったり=3")) #利用者の服のタイプを入力


def WaistRecvice(n):
    if n == 1: #測定者の服にゆとりがある場合
        waist = sokutei - yoyu_atumi
    elif n == 2: #服が普通くらいの場合
        waist = sokutei - hutu_atumi 
    elif n == 3: #服がぴったりの場合
        waist = sokutei - pita_atumi
    return waist