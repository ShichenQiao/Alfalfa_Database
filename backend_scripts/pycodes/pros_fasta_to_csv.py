import csv

def readFa(fa):
    with open(fa,'r') as FA:
        seqName,seq='',''
        while 1:
            line=FA.readline()
            line=line.strip('\n')
            if (line.startswith('>') or not line) and seqName:
                yield((seqName,seq))
            if line.startswith('>'):
                seqName = line[1:]
                seq=''
            else:
                seq+=line
            if not line:break

with open('protein_sequence.csv', 'w') as fp:
    content = csv.writer(fp)
    fa = "./MuXu_Last.pros.fasta"
    for seqName, seq in readFa(fa):
        content.writerow([seqName, seq])
    fp.close()


