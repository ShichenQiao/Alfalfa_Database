# https://blog.csdn.net/qq_18369669/article/details/103408600
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

fa="./ms.main.fasta"
for seqName,seq in readFa(fa):
    seqLen = len(seq)
    fileName = seqName + ".txt"
    file = open(fileName, 'w');
    file.write(seq)
    file.close()
    print(seqName,seqLen)