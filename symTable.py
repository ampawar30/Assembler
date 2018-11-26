sym_dict={}
def symT(dindx,name,size,tsize,sym,define,addr,cont):
    dict1={"Sym#"+str(dindx):{'Symname':name,'Size':size,'Tsize':tsize,'Sym/Label':sym,'Define':define,'Addr':addr,'Content':cont}}
    sym_dict.update(dict1)

def printSymT():
    print("SIndx\tName\tSize\tTSize\tSym/Lab\tDefine\tAddr\t\tContent")
    for indx,content in sym_dict.items():
        st=""
        st+=str(indx)+'\t'
        for key,val in content.items():
            st+=str(val)+'\t'
        print(st)

def symPresentN(label):
    flag=0
    for indx,content in sym_dict.items():
        for key,val in content.items():
            if key=='Symname' and label==val:
                flag=1
            elif key=='Define'and flag==1:
                sym_dict[indx][key]='D'
                flag=-1
                break
    if flag==1:
        return 0
    elif flag!=-1:
        return -1

def checkSym(symbol):
    strt=symbol.find('[')
    end=symbol.find(']')
    if strt==-1 and end==-1:
        s=symbol
    else:
        s=symbol[strt+1:end]

    for indx,content in sym_dict.items():
        for key,val in content.items():
            if key=='Symname':
                if s==val:
                    return indx
            else:
                break
    return symbol

def checkSym_opcode(searchL):
    for indx,content in sym_dict.items():
        if indx==searchL:
            for key,val in content.items():
                if key=='Addr':
                    return val


"""def printTable(dict):
    for s_id,sym_info in dict.items():
        print("\nS_id:",s_id)
        for key in sym_info:
            print(key+':'+str(sym_info[key]))
"""