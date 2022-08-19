import PySimpleGUI as sg

#結果を表示する関数

def result(h,k,w,m):#身長,肩幅,ウエスト,股下
    sg.theme("Dark Brown") #テーマの設定
    layout =  [[sg.Text(f"身長...{h}cm",font = ("", 50))],
              [sg.Text(f"肩幅...{k}cm",font = ("", 50))],
              [sg.Text(f"ウエスト...{w}cm",font = ("", 50))],
              [sg.Text(f"股下...{m}cm",font = ("", 50))],
              [sg.Button('終了')]]
              
    window = sg.Window("result_gui.py", layout)
    
    while True:
        event, values = window.read()
        if event in (None,'終了'): #終了ボタン、
            break
    window.close()