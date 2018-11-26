import re
import os
import litTable
import symTable
import calc_opcode

def writeLST(instrn):
    fp2=open("temp.lst","a+")
    fp2.writelines(instrn)
    fp2.close()

def get_hex(lit,flag):
    if flag==1:
        for indx,content in litTable.lit_dict.items():
            if indx==lit:
                for key,val in content.items():
                    if key=="LitHex":
                        str1=""
                        for i in range(len(val)):
                            str1+=val[i]
                        writeLST(str1+'\n')
                        return
    elif flag==-1:
        for indx,content in symTable.sym_dict.items():
            for key,val in content.items():
                if key=='Symname':
                    if val==lit:
                        writeLST(symTable.sym_dict[indx]['Addr']+'\n')
                break

def lstF(intermediate):
    os.remove("temp.lst")
    flag=mflag=0
    fp=open(intermediate,"r")
    for i in fp:
        rcnt=scnt=lcnt=0
        arr=i.split()
        if len(arr)>1:
            mainchk=bool(re.search('main:',arr[0].strip(),re.IGNORECASE))
        if mainchk==True:
            mflag=-1
        if len(arr)>1:
            m=bool(re.search('.data',arr[1],re.IGNORECASE))
            mm=bool(re.search('.bss',arr[1],re.IGNORECASE))
            mmm=bool(re.search('.text',arr[1],re.IGNORECASE))
            if m==True:
                flag=1
                continue    #skip section .data line
            elif mm==True:
                flag=-1
                continue
            elif mmm==True:
                flag=-2
                continue
            if flag==1:
                get_hex(arr[2],flag)
            elif flag==-1:
                get_hex(arr[0],flag)
            elif mflag==-1:
                rcnt=arr[1].count('Reg#')
                scnt=arr[1].count('Sym#')
                lcnt=arr[1].count('Lit#')
                opcode=calc_opcode.cal_op(arr[0].lower(),arr[1].split(","),rcnt,scnt,lcnt)
                writeLST(opcode+'\n')
        else:
            mflag=-1
    fp.close()
