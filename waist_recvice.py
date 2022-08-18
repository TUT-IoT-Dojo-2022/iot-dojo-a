yoyu_atumi = 10 #服の厚み平均
pita_atumi = 2 #ぴったりの場合の服の厚み
sokutei = 40 #センサーの値から計算したウエストの横幅

def main():
    n = int(input("余裕=1,ぴったり=2")) #利用者の服のタイプを入力


def WaistRecvice(n):
    if n == 1: #測定者の服にゆとりがある場合
        waist = sokutei - yoyu_atumi 
    else: #服がぴったりの場合
        waist = sokutei - pita_atumi
    return waist