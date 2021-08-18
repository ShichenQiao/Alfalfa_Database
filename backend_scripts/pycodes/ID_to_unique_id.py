import csv

with open('uniqueid_ID_primary.csv', 'r') as fp:
    reader = csv.reader(fp)
    rp = open('linkage_ID_to_uniqueid.csv', 'w')
    content = csv.writer(rp)
    temp = -1
    start = 1
    end = 1
    for x in reader:
        if x[0] == 1:
            name = x[1]
        if x[1] != temp:
            if temp != -1:
                print(name, 'starts from', start, 'ends at', end - 1)
                content.writerow([name,start,end - 1])
            name = x[1]
            start = int(x[0])
            temp = x[1]
        end = end + 1
    print(x[1], 'starts from', start, 'ends at', x[0])
    content.writerow([x[1], start, x[0]])

    fp.close()
    rp.close()

