import csv

with open("go_code.csv", 'r') as fp:
    reader = csv.reader(fp)
    rp = open("concatenated_go.csv", 'w')
    content = csv.writer(rp)
    for x in reader:
        temp = ""
        for letter in x[0]:
            if letter == '\t':
                temp = temp + ';'
            else:
                temp = temp + letter
        temp = temp.rstrip(";")
        content.writerow([temp])
    fp.close()
    rp.close()