
import PySimpleGUI as sg    

sg.theme('DarkAmber')   # デザインテーマの設定

itm = ["上着無し","上着あり"]
itm2 = ["ピッタリ","ふつう","上着無し"]

# ウィンドウに配置するコンポーネント
layout = [[sg.Listbox(itm ,size=(35,2),
                default_values=[["a"]],
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE),
                sg.Button("ok")]]

# ウィンドウの生成
window = sg.Window('採寸.beta', layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == None:
        break


window.close()