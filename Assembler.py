import symTable
import regTable
import litTable
import re
import lstFile

def findAttr(fname):
    fp=open(fname,"r")
    fp2=open("intermediate.txt","w+")
    name=size=ts=flag=mflag=0
    dindx=lindx=-1
    ddcnt=dbcnt=cnt=dqcnt=0
    for i in fp:
        arr=i.split(" ",1)
        mainchk=bool(re.search('main:',arr[0].strip(),re.IGNORECASE))
        if mainchk==True:
            mflag=-1
        if len(arr)>1:
            #errTable.findErr(arr[0].strip())
            m=bool(re.search('.data',arr[1],re.IGNORECASE))
            mm=bool(re.search('.bss',arr[1],re.IGNORECASE))
            mmm=bool(re.search('.text',arr[1],re.IGNORECASE))
            if m==True:
                flag=1
                fp2.writelines(i)
                continue 
            elif mm==True:
                flag=-1
                ts=0
                fp2.writelines(i)
                continue
            elif mmm==True:
                flag=-2
                fp2.writelines(i)
                continue
            if flag==1:
                if (arr[1][:2]).lower()=='dd': #check 1st two char
                    name=arr[0].strip()
                    size=4
                    cnta=arr[1][3:].split(",")
                    ddcnt+=int(len(cnta))
                    lindx+=1
                    cnta=litTable.litT(lindx,cnta,1)
                    fp2.writelines(name+' '+'dd'+' '+cnta+'\n')
                    dindx+=1
                    if len(hex(ts))>3:
                        addr=(hex(ts)[2:]).upper()+"000000"
                    else:
                        addr="0"+(hex(ts)[2:]).upper()+"000000"
                    symTable.symT(dindx,name,size,ddcnt,'S','D',addr,cnta)
                    ts+=ddcnt*int(size)
                    ddcnt=0
                elif (arr[1][:2]).lower()=='db':
                    name=arr[0].strip()
                    size=1
                    arr1=arr[1][3:]
                    for k in range(len(arr1)):
                        if arr1[k]=='"' or arr1[k]=="'":
                            cnt+=1
                        elif cnt==1 and arr1[k]!='\n\t':
                            dbcnt+=1
                        elif cnt==2 or cnt==0:
                            if arr1[k]!=',' and arr1[k]!='1' and arr1[k]!='\n':
                                dbcnt+=1
                   
                    lindx+=1
                    arr1=litTable.litT(lindx,arr1,-1)
                    fp2.writelines(name+' '+'db'+' '+arr1+'\n')
                    dindx+=1
                    
                    if len(hex(ts))>3:
                        addr=(hex(ts)[2:]).upper()+"000000"
                    else:
                        addr="0"+(hex(ts)[2:]).upper()+"000000"
                    symTable.symT(dindx,name,size,dbcnt,'S','D',addr,arr1)
                    ts+=dbcnt*int(size)
                    dbcnt=cnt=0
                elif (arr[1][:2]).lower()=='dq':
                    name=arr[0].strip()
                    size=8
                    cnta=arr[1][3:].split(",")
                    dqcnt+=int(len(cnta))
                    lindx+=1
                    cnta=litTable.litT(lindx,cnta,1)
                    fp2.writelines(name+' '+'dq'+' '+cnta+'\n')
                    dindx+=1
                    if len(hex(ts))>3:
                        addr=(hex(ts)[2:]).upper()+"000000"
                    else:
                        addr="0"+(hex(ts)[2:]).upper()+"000000"
                    symTable.symT(dindx,name,size,dqcnt,'S','D',addr,cnta)
                    ts+=dqcnt*int(size)
            elif flag==-1:
                if (arr[1][:4]).lower()=='resd':
                    name=arr[0].strip()
                    size=4
                    tsize=arr[1][5:].strip()
                    fp2.writelines(i)
                    dindx+=1
                    if len(hex(ts))>3 and len(hex(ts))<5:
                        addr=(hex(ts)[2:]).upper()+"000000"
                    elif len(hex(ts))>4:
                        addr=(hex(ts)[2:]).upper()+"00000"
                    else:
                        addr="0"+(hex(ts)[2:]).upper()+"000000"
                    symTable.symT(dindx,name,size,tsize,'S','D',addr,'-')
                    ts+=int(tsize)*int(size)
                elif (arr[1][:4]).lower()=='resq':
                    name=arr[0].strip()
                    size=8
                    tsize=arr[1][5:].strip()
                    fp2.writelines(i)
                    dindx+=1
                    symTable.symT(dindx,name,size,tsize,'S','D',hex(ts)[2:],'-')
                    ts+=int(tsize)*int(size)
        if len(arr)==1 and arr[0].strip():
            mflag=-1
        if mflag==0 and flag==-2:
            fp2.writelines(i)
        if mflag==-1:
            fp2.close()
            dindx=findLables(arr,dindx)
            dindx,lindx=regTable.regT(arr,dindx,lindx)

    print("Symbol Table\n")
    symTable.printSymT()
    print("\tLiteral Table\n")
    litTable.printLitT()
    fp.close()
    lstFile.lstF("intermediate.txt")

def findLables(arr,dindx):
    for i in range(len(arr)):
        index=arr[i].find(':')
        if index>-1:
            label=(arr[i][:index].strip())
            rval=symTable.symPresentN(label)
            if rval==-1:
                dindx+=1
                symTable.symT(dindx,label,0,0,'L','D','-','-')
                return dindx
    return dindx 

import sys
fname=sys.argv[1]
findAttr(fname)
