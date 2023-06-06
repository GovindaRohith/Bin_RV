#Code by Govinda Rohith Y
#CS21BTECH11062
#Computer Architecture - CS2323
#Lab-8/Exam (RISC-V Disassembler)
import sys
def u_type(bin,is_one): #For U-Type instructions
    rd=int(bin[20:25],2)
    imm=bin[0:20]
    imm=hex(int(imm, 2))
    if(is_one):   print("lui",end=" ")
    else:         print("auipc",end=" ")
    print("x",end="")
    print(rd,end=" ")
    print(imm)
    
def j_type(bin): #For J-Type instructions
    rd=int(bin[20:25],2)
    sign=int(bin[0:1],2)
    imm=int(bin[12:20]+bin[11:12]+bin[1:11]+"0",2)
    imm=imm-sign*pow(2,20)
    print("jal x",end="")
    print(rd,end=" ")
    return imm

def b_type(bin): #For Branching(B-Type) instructions
    f_3=bin[17:20]
    rs1=int(bin[12:17],2)
    rs2=int(bin[7:12],2)
    sign=int(bin[0:1],2)
    imm=int(bin[24:25]+bin[1:7]+bin[20:24]+"0",2)
    imm=imm-sign*pow(2,12)
    if f_3=="000":    print("beq",end=" ")
    elif f_3=="001":  print("bne",end=" ")
    elif f_3=="100":  print("blt",end=" ")
    elif f_3=="101":  print("bge",end=" ")
    elif f_3=="110":  print("bltu",end=" ")
    elif f_3=="111":  print("bgeu",end=" ")
    else:
        print("Invalid Opcode")
        return -1
    print("x",rs1," x",rs1," ",sep="",end="")
    return imm

def s_type(bin): #For S-Type Instructions
    f_3=bin[17:20]
    rs1=int(bin[12:17],2)
    rs2=int(bin[7:12],2)
    imm=bin[1:7]+bin[20:25]
    sign=int(bin[0:1])
    imm=int(imm,2)
    imm=imm-sign*pow(2,11)
    if f_3=="000":   print("sb",end=" ")
    elif f_3=="001": print("sh",end=" ")
    elif f_3=="010": print("sw",end=" ")
    elif f_3=="011": print("sd",end=" ")
    else:
        print("Invalid input")
        return False
    print("x",rs2," ",imm,"(x",rs1,")",sep="")
    return bin

def i_type_load(bin): #For I-Type class of load instructions 
    f_3=bin[17:20]
    rs1=int(bin[12:17],2)
    rd=int(bin[20:25],2)
    sign=int(bin[0:1])
    rem=bin[1:12]
    rem=int(rem,2)
    imm=rem-sign*pow(2,11)
    if f_3=="000":   print("lb",end=" ")
    elif f_3=="001": print("lh",end=" ")
    elif f_3=="010": print("lw",end=" ")
    elif f_3=="011": print("ld",end=" ")
    elif f_3=="100": print("lbu",end=" ")
    elif f_3=="101": print("lhu",end=" ")
    elif f_3=="110": print("lwu",end=" ")
    else:
        print("Invalid Input")
        return False
    print("x",rd," ",imm,"(x",rs1,")",sep="")
    return bin

def i_type_reg(bin,is_jalr):  #For I-Type class of non-load instructions and jalr 
    f_3=bin[17:20]
    rs1=int(bin[12:17],2)
    rd=int(bin[20:25],2)
    sign=int(bin[0:1])
    rem=bin[1:12]
    rem=int(rem,2)
    imm=rem-sign*pow(2,11)
    temp=bin[0:6]
    if(is_jalr):
        print("jalr x",end="")
        if(rs1==rd and rs1==1):
            print(rs1,end="")
        else:
            print(rd,end=" ")
            print("x",end="")
            print(rs1,end=" ")
        if(imm!=0): print(imm)
        else: print()
        return True
    if f_3=="000": print("addi",end=" ")    
    elif f_3=="100": print("xori",end=" ")   
    elif f_3=="110": print("ori",end=" ")   
    elif f_3=="111": print("andi",end=" ") 
    elif f_3=="001" and temp=="000000": 
        imm=int(bin[6:12],2)
        if(imm<0 or imm>=64):
            print("Invalid opcode ")
            return False
        print("slli",end=" ")
    elif f_3=="101" and temp=="000000":
        imm=int(bin[6:12],2)
        if(imm<0 or imm>=64):
            print("Invalid opcode ")
            return False
        print("srli",end=" ")
    elif f_3=="101"and temp=="010000":
        imm=int(bin[6:12],2)
        if(imm<0 or imm>=64):
            print("Invalid opcode ")
            return False
        print("srai",end=" ")
    elif f_3=="010": print("slti",end=" ")
    elif f_3=="011": print("sltiu",end=" ")        
    else:
        print("Invalid input")
        return False
    print("x",rd," x",rs1," ",imm,sep="")
    return True

def r_type(bin): #For R-Type instructions
    f_3=bin[17:20]
    f_7=bin[0:7]
    rs1=int(bin[12:17],2)
    rs2=int(bin[7:12],2)
    rd=int(bin[20:25],2)
    if f_3=="000" and f_7=="0000000":    print("add",end=" ")
    elif f_3=="000" and f_7=="0100000":  print("sub",end=" ")
    elif f_3=="100" and f_7=="0000000":  print("xor",end=" ")
    elif f_3=="110" and f_7=="0000000":  print("or",end=" ")
    elif f_3=="111" and f_7=="0000000":  print("and",end=" ")
    elif f_3=="001" and f_7=="0000000":  print("sll",end=" ")
    elif f_3=="101" and f_7=="0000000":  print("srl",end=" ")
    elif f_3=="101" and f_7=="0100000":  print("sra",end=" ")
    elif f_3=="010" and f_7=="0000000":  print("slt",end=" ")
    elif f_3=="011" and f_7=="0000000":  print("sltu",end=" ")        
    else :
        print("Invalid input")
        return False
    print("x",rd," x",rs1," x",rs2,sep="")
    
def op_sep(bin): #Function to call above functions according to instructions
    opc=bin[25:32]
    if len(bin)!=32:
        print("Invalid Input")
        return -1
    if opc=="0110011":      r_type(bin)
    elif opc=="0010011":    i_type_reg(bin,False)
    elif opc=="0000011":    i_type_load(bin)
    elif opc=="0100011":    s_type(bin)
    elif opc=="1100011":    return b_type(bin)
    elif(opc=="1101111"):   return j_type(bin) 
    elif (opc=="1100111"):  i_type_reg(bin,True) #jalr
    elif (opc=="0110111" ): u_type(bin,True) #lui
    elif (opc=="0010111"):  u_type(bin,False) #auipc
    else :         print("Invalid input")
    return -1

def hex_to_bin(str): #Function to convert hexadecimal string to binary string
   return bin(int(str, 16))[2:].zfill(32) 

#main
pc=0
arr=[]
arr.append(0)
# print("********Without Lables **********")
f = open("input.txt", "r")
o=open("wo_labels.txt","w")
sys.stdout = o
while True:
    str=f.readline().strip()
    if not str: break
    str=hex_to_bin(str)
    req=op_sep(str) 
    if req!=-1:
        arr.append(pc+req)
        print(req)
    pc=pc+4
f.close()
o.close()
o=open("wi_labels.txt","w")
sys.stdout = o
arr=[*set(arr)]
arr.sort()
# print("******* With Lables  *********")
pc=0
index=0
f = open("input.txt", "r")
while True:
    if arr[index]>=0: break
    else :
        arr.remove(arr[index])
while True:
    if index<len(arr) and pc==arr[index]:
        print("L",index,":",sep="")
        index=index+1
    str=f.readline().strip()
    if not str: break
    str=hex_to_bin(str)
    req=op_sep(str) 
    if req!=-1:
        try:
            print("L",arr.index(pc+req),sep="")
        except:
            print(pc+req)
            print("#Branching is taking out of limits so printing the immediate value only")
    pc=pc+4
f.close()
o.close()