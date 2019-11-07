

def not_num(content):
    if content == "0":
        return 0
    if content == "1":
        return 0
    if content == "2":
        return 0
    if content == "3":
        return 0
    if content == "4":
        return 0
    if content == "5":
        return 0
    if content == "6":
        return 0
    if content == "7":
        return 0
    if content == "8":
        return 0
    if content == "9":
        return 0
    if content == "-":
        return 0
    return 1


def read_file_spice(filename):
    file = open(filename,'r')
    lines = file.readlines()
    #print(lines)
    #return 0
    total_data = []
    target_str = "Step Information"
    i = 2
    while i < len(lines):
        data = {"f":[], "abs":[], "pha": []}

        while i < len(lines) and (len(lines[i]) < len(target_str) or lines[i][:len(target_str)] != target_str):
            pnt = 0
            c1 = ""
            c2 = ""
            c3 = ""
            while lines[i][pnt] != '\t':
                c1 += lines[i][pnt]
                pnt += 1

            while not_num(lines[i][pnt]):
                pnt += 1

            while lines[i][pnt] != 'd':
                c2 += lines[i][pnt]
                pnt += 1
            pnt += 1
            while not_num(lines[i][pnt]):
                pnt += 1
            while lines[i][pnt] != '°':
                c3 += lines[i][pnt]
                pnt += 1

            c1 = float(c1)
            c2 = float(c2)
            c3 = float(c3)

            data["f"].append(c1)
            data["abs"].append(c2)
            data["pha"].append(c3)
            i += 1
        total_data.append(data)
        i += 1
    return total_data


#data = read_file_spice("EJ1/Circuito con Legendre/Simulacion/BodeMontecarlo.txt")
#print(len(data))

