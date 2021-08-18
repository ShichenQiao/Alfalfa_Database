import csv

with open("pathway_code.csv", 'r') as fp:
    reader = csv.reader(fp)
    rp = open("concatenated_pathway.csv", 'w')
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
        print(temp)

    fp.close()
    rp.close()