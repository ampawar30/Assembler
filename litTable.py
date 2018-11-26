lit_dict={}

def no_to_hex(content,arr):
    if len(content)>=1:
        for i in range(len(content)):
            hexval=hex(int(content[i].strip()))
            if len(hexval)>3:
                hexval=hexval[2:]+"000000"
            else:
                hexval='0'+hexval[2:]+"000000"
            arr.append(hexval.upper())

def str_to_hex(content,arr):
    cnt=flag=0
    for i in range(len(content)):
        if content[i]=='"' or content[i]=="'":
            cnt+=1
        elif cnt==1:
            k=hex(ord(content[i]))
            arr.append(k[2:].upper())
        elif cnt==2 or cnt==0:
            if content[i]!=',' and content[i]!='\n':
                if content[i]=='1':
                    arr.append('0A')
                    flag=1
                    i+=2
                elif flag==0:
                    arr.append('00')
            else:
                flag=0

def litT(lindx,content,flag):
    arr=[]
    if flag==1:
        no_to_hex(content,arr)
    elif flag==-1:
        str_to_hex(content,arr)
    tempdict={"Lit#"+str(lindx):{'LitHex':arr,'LitContent':content}}
    lit_dict.update(tempdict)
    return "Lit#"+str(lindx)

def checkLit(searchLit):
    for indx,content in lit_dict.items():
        for key,val in content.items():
            if key=='LitContent':
                if searchLit==val:
                    return indx
    return -1

def checkLit_opcode(searchL):
    for indx,content in lit_dict.items():
        if indx==searchL:
            for key,val in content.items():
                if key=='LitHex':
                    return val[0]

def printLitT():
    print("LIndx\t\t\tLHex\t\t\tLContent")
    for indx,content in lit_dict.items():
        st=""
        st+=str(indx)+'\t'
        for key,val in content.items():
            st+=str(val)+'\t'
        print(st)
