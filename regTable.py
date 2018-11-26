import symTable
import litTable
import re

reg={'eax':'Reg#0','ecx':'Reg#1','edx':'Reg#2','ebx':'Reg#3','esp':'Reg#4','ebp':'Reg#5','esi':'Reg#6','edi':'Reg#7'}
def regT(instrn,dindx,lindx):
    fp=open("intermediate.txt","a+")
    flag=valflag=0
    i=len(instrn)
    if i>1:
        m=bool(re.search('printf',instrn[1].strip(),re.IGNORECASE))
        mm=bool(re.search('puts',instrn[1].strip(),re.IGNORECASE))
        if m==True or mm==True:
            str1=instrn[0]+' '+instrn[1]
            fp.writelines(str1)
        for key in reg:
            val=instrn[1].__contains__(key)
            if val==True:
                valflag=1
                str1=""
                str1+=instrn[0].strip()+' '
                chk=instrn[1].strip().split(",")
                for j in range(len(chk)):
                    fst=chk[j].find('[')
                    dword=chk[j][:fst+1]
                    if j==0:
                        if key==chk[j].strip():
                            str1+=reg.get(key)
                        elif chk[j].__contains__(key) and fst>-1:
                            str1+=dword+reg.get(key)+']'
                        else:
                            indx=""
                            indx=symTable.checkSym(chk[j].strip())
                            if indx!=chk[j].strip() and fst==-1:
                                str1+=indx+'\n'
                            elif indx!=chk[j].strip() and fst>-1:
                                str1+=dword+indx+']'
                            else:
                                for r,v in reg.items():
                                    if r==chk[j].strip():
                                        str1+=v
                                        break
                        if(len(chk)==1):
                            fp.write(str1+'\n')
                    elif j>0:
                        for r in reg:
                            if r==chk[j].strip():
                                if fst==-1:
                                    str1+=','+reg.get(r)+'\n'
                                elif fst>-1:
                                    str1+=','+reg.get(r)+']\n'
                                flag=1
                                break
                            elif chk[j].__contains__(key) and fst>-1:
                                str1+=dword+reg.get(key)+']\n'
                                flag=1
                                break
                            else:
                                flag=0
                        if flag==0:
                            indx=""
                            indx=symTable.checkSym(chk[j].strip())
                            if indx!=chk[j].strip():
                                if fst==-1:
                                    str1+=','+dword+indx+'\n'
                                elif fst>-1:
                                    str1+=','+dword+indx+']\n'
                            else:
                                indx=litTable.checkLit([chk[j].strip()])
                                if indx==-1:
                                    lindx+=1
                                    indx=litTable.litT(lindx,[chk[j].strip()],1)
                                str1+=','+indx+'\n'
                        fp.writelines(str1)
                break
        if valflag==0:
            indx=str1=""
            indx=symTable.checkSym(instrn[1].strip())
            if indx!=(instrn[1].strip()):
                str1=instrn[0].strip()+' '+indx+'\n'
                fp.writelines(str1)
            else:
                if instrn[0].strip()=='jz' or instrn[0].strip()=='jmp' or instrn[0].strip()=='je' or instrn[0].strip()=='jne':
                    dindx+=1
                    symTable.symT(dindx,instrn[1].strip(),0,0,'L','U','-','-')
                    indx=symTable.checkSym(instrn[1].strip())
                    if indx!=(instrn[1].strip()):
                        str1=instrn[0].strip()+' '+indx+'\n'
                        fp.writelines(str1)
    else:
        str1=""
        if instrn[0]!='\n':
            str1+=instrn[0]
            fp.write(str1)
    fp.close()
    return dindx,lindx