clh1_pittari = []
clh1_hodoyoi = []
clh1_over = []
with open("./files/clothes1.txt") as f:
    list_line = f.readlines()
    for l in list_line:
        if l[:-1] == "\n":
            l = int(l[:-1])
        else:
            l = int(l)
        if 20 < l:
            clh1_over.append(str(l)+"\n")
        elif 10 < l:
            clh1_hodoyoi.append(str(l)+"\n")
        else:
            clh1_pittari.append(str(l)+"\n")

clh2_pittari = []
clh2_hodoyoi = []
clh2_over = []
with open("./files/clothes2.txt") as f:
    list_line = f.readlines()
    for l in list_line:
        if l[:-1] == "\n":
            l = int(l[:-1])
        else:
            l = int(l)
        if 20 < l:
            clh2_over.append(str(l)+"\n")
        elif 10 < l:
            clh2_hodoyoi.append(str(l)+"\n")
        else:
            clh2_pittari.append(str(l)+"\n")

with open("./files/clh1_hodoyoi.txt", mode='w') as f:
    f.writelines(clh1_hodoyoi)

with open("./files/clh1_pittari.txt", mode='w') as f:
    f.writelines(clh1_pittari)

with open("./files/clh1_over.txt", mode='w') as f:
    f.writelines(clh1_over)

with open("./files/clh2_hodoyoi.txt", mode='w') as f:
    f.writelines(clh2_hodoyoi)

with open("./files/clh2_pittari.txt", mode='w') as f:
    f.writelines(clh2_pittari)

with open("./files/clh2_over.txt", mode='w') as f:
    f.writelines(clh2_over)