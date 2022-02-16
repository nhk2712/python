def splitName(name):
    nlist=name.split()
    
    last=nlist[len(nlist)-1]
    nlist.pop(len(nlist)-1)

    res=" ".join(nlist)
    res+=","+last

    return res

src= open('tmp.txt','r+t',encoding='UTF-8')

res=""
while True:
    line=src.readline()
    if not line: break

    line=splitName(line)
    res+=line+"\n"

src.close()

out=open('out.csv','w',encoding='UTF-8')
out.write(res)
out.close()