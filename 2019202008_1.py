import sys

enum = dict(read ="READ", write = "WRITE", output="OUTPUT",commit="COMMIT",start="START", default="DEFAULT")

def assign_operator(exression):
    operation = ''
    if('+' in exression):
        operation='+'
    elif('/' in exression):
        operation='/'
    elif('-' in exression):
        operation='-'
    elif('*' in exression):
        operation='*'
    return operation

def return_slice(expression):
    expression = expression[:-1]
    return expression

def write_to_disk(output_file,memory_variables,disk_variables):
    var1 = ""
    var2 = ""
    sort_var1 = sorted(memory_variables)
    for i in sort_var1:
        t1 = i + " "
        t2 = t1 + str(memory_variables[i])+" "
        var1 = var1 + t2
    var1=return_slice(var1)

    sort_var2 = sorted(disk_variables)
    for i in sort_var2:
        t1 = i + " "
        t2 = t1 + str(disk_variables[i])+" "
        var2 = var2 + t2
    var2=return_slice(var2)
    output_file.write(var1+"\n")
    output_file.write(var2+"\n")

def assign_to_disk_variables(variables,t1):
    e_variables = variables[0::2]
    o_values = variables[1::2]
    for j in range(len(e_variables)):
        t1[e_variables[j]] = int(o_values[j])
    return t1

def check_break(t1):
    flag = 0
    for i,j in t1.items():
        if j==False:
            flag = 1
    if flag == 0:
        return True
    else:
        return False

def increment_cur_i(t1,t2,t3,t4):
    temp = t4%len(t1)
    if temp == 0:
        t2 = t2 +t3
        t4=0
    return t2,t4

def initialize_all_trans(expression,t2):
    entities = expression.split(" ")
    trans = entities[0]
    e = entities[1]
    t2.append(trans)
    return t2,trans,e

def check_if_tran(e):
    t1 = e.split(" ")[0]
    t1_1 = t1[0]
    if(t1_1 == 'T'):
        return True
    else:
        return False

def get_indices(exp):
    start = exp.find("(")+1
    mid1 = exp.find(",")
    mid2 = exp.find(",")+1
    end = exp.find(")")
    return start,mid1,mid2,end

def reshape_instruction(e):
    e = e.strip()
    e = e.replace(" ","")
    t = e.split("(")[0]
    op = ""
    if(t == enum['read']):
        op = enum['read']
    elif(t == enum['write']):
        op = enum['write']
    elif(t == enum['output']):
        op = enum['output']
    else:
        op = enum['default']
    return e,op

def form_string(command,exp):
    start = "<"+command+" "
    mid = start + exp+">"
    close = mid + "\n"
    return close

def initialize_variable(expression,t2,t3,t4): 
    t2,trans,e=initialize_all_trans(expression,t2)
    t4[trans] = list()    
    t3[trans] = int(e)
    return t2,t3,t4, trans
    
def read_operation(expression,t1,t2,t3,t4):
    start,mid1,mid2,end = get_indices(expression)
    x1 = expression[start:mid1]
    x2 = expression[mid2:end]
    if (x1 in t1.keys()):
        t2[x2] = t4[x1]
        t1[x1] = x2
    else:
        t1[x1] = x2
        t2[x2] = t3[x1]
        t4[x1] = t3[x1]

    return t1,t2,t3,t4

def check_read_output_write(expression):
    if(expression.split("(")[0] == enum['read']):
        return True
    elif(expression.split("(")[0] == enum['output']):
        return True
    elif(expression.split("(")[0] == enum['write']):
        return True
    return False

def write_operation(expression,output_file,t1,t2,t3,t4):
    start,mid1,mid2,end=get_indices(expression)
    x1 = expression[start:mid1]
    x2 = expression[mid2:end]
    temp1 = "<"+t1+", "
    temp2 = temp1+x1+", "
    temp3 = temp2 + str(t2[x1])+">"
    output_file.write(temp3+"\n")
    t2[x1] = int(t3[x2])
    write_to_disk(output_file,t2,t4)
    return t2,t3,t4

def output_operation(expression,t1,t2):
    start = expression.find("(")+1
    end  = expression.find(")")
    variable = expression[start:end]
    t2[variable]=t1[variable]
    return t1, t2

def default_operation(expression,t1):
    end1 = expression.find(":")
    start1 = expression.find("=")+1
    operation = assign_operator(expression)
    end2 = expression.find(operation)
    start2 = expression.find(operation)+1
    variable_1 = expression[0:end1]
    variable_2 = expression[start1:end2]
    value = expression[start2:]
    a = t1[variable_2]
    b = int(value)
    c = 0
    if operation == '+':
        c = a+b
    if operation == '-':
        c = a-b
    if operation == '*':
        c = a*b
    if operation =='/':
        c = float(a)/float(b)
    t1[variable_1] = c
    return t1

def undo_logging(x,output_file,transactions,disk_variables,all_transactions,transaction_list):
    memory_variables = {}
    completed_transactions = {}
    variable_and_value = {}
    varaibles_temp = {}

    for j in transactions.keys():
        completed_transactions[j]=False
    k=0
    present = transaction_list[k]
    cur=0
    while True:
        if (cur >= all_transactions[present]):
            completed_transactions[present]=True

        elif(cur < all_transactions[present]):    
            exressions = transactions[present]
            end_cur = cur+x
            exressions = exressions[cur:end_cur]

            if cur==0:
                exp = form_string(enum['start'],present)
                output_file.write(exp)
                write_to_disk(output_file,memory_variables,disk_variables)

            for expression in exressions:
                expression,operation = reshape_instruction(expression)
                if (operation == enum['read']):
                    variable_and_value,varaibles_temp,disk_variables,memory_variables = read_operation(expression,variable_and_value,varaibles_temp,disk_variables,memory_variables)
                elif(operation == enum['write']):
                    memory_variables,varaibles_temp,disk_variables = write_operation(expression,output_file,present,memory_variables,varaibles_temp,disk_variables)
                elif(operation == enum['output']):
                    memory_variables, disk_variables = output_operation(expression,memory_variables,disk_variables)
                elif(operation == enum['default']):
                    varaibles_temp = default_operation(expression,varaibles_temp)

            if end_cur >= all_transactions[present]:
                exp = form_string(enum['commit'],present)
                output_file.write(exp)
                write_to_disk(output_file,memory_variables,disk_variables)


        k = k+1
        cur,k = increment_cur_i(transactions,cur,x,k)
        present = transaction_list[k]
        if(check_break(completed_transactions)):
            break

def main():
    transactions = {}
    disk_variables = {}
    all_transactions = {}
    transaction_list = []

    input_file = sys.argv[1]
    x = int(sys.argv[2])
    flag = 0
    trans = ""
    for expression in open(input_file):
        if flag == 0:
            exps = expression.split()
            disk_variables = assign_to_disk_variables(exps,disk_variables)
            flag=1
        elif(check_if_tran(expression)):
            transaction_list,all_transactions,transactions, trans = initialize_variable(expression,transaction_list,all_transactions,transactions)
        elif(check_read_output_write(expression)):
            transactions[trans].append(return_slice(expression))
        elif expression.strip() == "":
            trans = ""
        else:
            transactions[trans].append(return_slice(expression))
        
    
    output_file = open("2019202008_1.txt","w") 
    undo_logging(x,output_file,transactions,disk_variables,all_transactions,transaction_list)
    output_file.close()

if __name__ == "__main__":
    main()