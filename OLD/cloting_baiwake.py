pittari_size = [10, 10]
hodoyoi_size = [18, 16, 14, 13, 19, 16, 14, 16, 12, 14, 12]
over_size = [26, 22, 20, 20, 26, 24, 24] 
L = 0 #ウエストの計測値
pittari_size_ave = sum(pittari_size) / len(pittari_size)
hodoyoi_size_ave = sum(hodoyoi_size) / len(hodoyoi_size)
over_size_ave = sum(over_size) / len(over_size)
clothing_size = int(input("1:ぴちぴちサイズ,2:ちょうどいいサイズ,3:オーバサイズから数字を1つ選んでください."))
if clothing_size == 1:
    L = L - pittari_size_ave
elif clothing_size == 2:
    L = L - hodoyoi_size_ave
elif clothing_size == 3:
    L = L - over_size_ave
print(L)