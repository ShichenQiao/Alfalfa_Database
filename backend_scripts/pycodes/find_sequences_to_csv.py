import csv

with open('start_end_raw.csv', 'r') as fp:
    reader = csv.reader(fp)
    sp = open('sequences.csv', 'w')
    content = csv.writer(sp)
    f = open('Chr1.txt', 'r')
    for x in reader:
        unique_id = x[0]
        seqName = x[1]
        start = x[2]
        end = x[3]
        fileName = seqName + '.txt'
        print(unique_id)
        f = open(fileName, "r")
        data = f.read()
        f.close()
        seq = data[int(start) - 1:int(end)]
        content.writerow([unique_id, seq])
        print(seq.__len__())
    f.close()
    fp.close()
    sp.close()
