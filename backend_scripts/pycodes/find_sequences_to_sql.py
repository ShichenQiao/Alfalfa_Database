import csv

with open('start_end_raw.csv', 'r') as fp:
    reader = csv.reader(fp)
    rf = open('sequences.sql', 'w')
    f = open('Chr1.txt', 'r')
    for x in reader:
        unique_id = x[0]
        seqName = x[1]
        start = x[2]
        end = x[3]
        fileName = seqName + '.txt'
        f = open(fileName, "r")
        data = f.read()
        f.close()
        seq = data[int(start) - 1:int(end)]
        sql = "UPDATE gff SET DNA = '" + seq + "' WHERE unique_id = '" + unique_id + "';\n"
        rf.write(sql)
        print(unique_id)
    f.close()
    fp.close()
    rf.close()
