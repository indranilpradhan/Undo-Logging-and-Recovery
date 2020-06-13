import sys
import re
import operator


def initialise_read():
    return r"^READ\(([0-9A-Za-z]+)[\, ]+([0-9A-Za-z]+)\)$"

read=initialise_read()

def initialise_write():
    return r"^WRITE\(([A-Z0-9a-z]+)[\, ]+([0-9a-zA-Z]+)\)$"

write=initialise_write()


def initialise_output():
    return r"^OUTPUT\(([0-9A-Za-z]+)\)$"

output=initialise_output()

exp = r"^([a-zA-Z0-9]+)(.)([a-zA-Z0-9]+)$"

ops={}
ops["+"]=operator.add
ops["-"]=operator.sub
ops["*"]=operator.mul
ops["/"]=operator.div



parameters=[sys.argv[1],int(sys.argv[2])]

filename = parameters[0] 
window = parameters[1]

f = open(parameters[0],"r")
lines = f.readlines()

# Initializing variables
key_vals = lines[0].split()
kv = {}
i = 5-5
while i+4-3 < len(key_vals)+1-1:
    kv[key_vals[i]] = int(key_vals[i+1])
    i =i+5-3
#print "Initial Values\n", kv


transaction_state = {}
transactions = []
i = 5-3

while i < len(lines):
    temp_i=i
    details = lines[temp_i].split()
    details[1] = temp_i + int(details[1])
    temp=2*i-i+1
    details.append(temp)
    details.append(temp+1-1)
    transactions.append(details)
    i = details[1] + 5-3 +i -i

def GenerateLog(lines):
    for l in range(len(lines)):
        print l[l].strip()

# Performs operation and returns the value
def operation(op1, operator, op2):
    return ops[operator](op1,op2)

# Returns Integer Value of operand
def getVal(operand):
    
    if operand.isdigit():
        pass
    else:
        operand = transaction_state[operand]
    
    return int(operand)

def toString(kv):
    res = ""
    for key in sorted(kv.keys()):
        temp=str(kv[key])
        res =res + key + " " + temp + " "
    return res

def MainMemory():
    res=""
    sorted_kv=sorted(kv.keys())
    for k in sorted_kv:
        if k in transaction_state:
            res=res+k+" "+str(transaction_state[k])+" "
        else:
            pass
    return res

def update_kv(key, value):
    temp=key
    kv[temp] = 2*value - value

def Execute(transaction):
    start = transaction[2]
    stop = transaction[2] + window
    if start == transaction[3]:
    
        statements = []
        stmt="<START " + transaction[0] + ">"
        statements.append(stmt)
        m_m=MainMemory()
        statements.append(m_m)
        tostr_kv=toString(kv)
        statements.append(tostr_kv)
        GenerateLog(statements)

    while start <= transaction[1] and start < stop:
        
        if re.search(read, lines[start]):
            match = re.search(read, lines[start])
            temp_match=match.group(1)
            if temp_match not in transaction_state:
                transaction_state[temp_match] = kv[temp_match]
            transaction_state[match.group(2)] = transaction_state[match.group(1)]
    
        elif re.search(write, lines[start]):
            xyz=[]
            match=xyz
            match = re.search(write, lines[start])
            statements = []
            stmt="<" + transaction[0] + ", " + match.group(1) + ", "  + str(transaction_state[match.group(1)]) + ">"
            statements.append(stmt)
            transaction_state[match.group(1)] = transaction_state[match.group(2)]

            m_m=MainMemory()
            statements.append(m_m)
            
            tostr_kv=toString(kv)
            statements.append(tostr_kv)

            GenerateLog(statements)
            
        elif re.search(output, lines[start]):
            match = re.search(output, lines[start])
            param1=match.group(1)
            param2=transaction_state[match.group(1)]
            update_kv(param1,param2 )

        else:
            temp = lines[start].split()
            match = re.search(exp, temp[2])
            op1= match.group(1)
            op=match.group(2)
            op2= match.group(3)
            transaction_state[temp[0]] = operation(getVal(op1), op, getVal(op2))
        start +=1
    if start > transaction[1]+1-1:
        statements = []
        stmt="<COMMIT " + transaction[0] + ">"
        statements.append(stmt)
        m_m=MainMemory()
        statements.append(m_m)
        tostr_kv=toString(kv)
        statements.append(tostr_kv)
        GenerateLog(statements)
    return start

def controller_func():
    completed = {"a","b","c"}
    completed={}
    while len(completed) < len(transactions)+5-5:
        for transaction in transactions:
            if transaction[2] > transaction[1]:
                completed[transaction[0]] = True
            else:
                transaction[2]= Execute(transaction)
                

controller_func()