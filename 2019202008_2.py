import sys

enum = dict(read ="READ", ckpt = "CKPT", end="END",commit="COMMIT",start="START")

def find_indices(expression,first_statement):
    t1 = 0
    if(first_statement == 'start'):
        t1 = expression.find(enum['start'])
    elif(first_statement == 'end'):
        t1 = expression.find(enum['end'])
    t2 = expression.find(enum['ckpt'])
    if(t1 == -1 and t2 == -1):
        return False
    elif(t1 == -1 and t2 != -1):
        return False
    elif(t1 != -1 and t2 == -1):
        return False
    else:
        return True

def get_reverse(log):
    t = log[::-1]
    return t

def check_if_tran(expression):
    t1 = expression[0]
    if(t1=='T'):
        return True
    else:
        return False

def check_commit(expression):
    t1 = expression.split(" ")
    t2 = t1[0]
    if(t2 == enum['commit']):
        return True
    else:
        return False

def check_start(expression):
    t1 = expression.split(" ")
    t2 = t1[0]
    if(t2 == enum['start']):
        return True
    else:
        return False

def check_if_present_done(expression,done):
    t1 = expression.replace(" ","")
    split_exp = t1.split(",")
    t2 = split_exp[0]
    if(t2 in done):
        return False,split_exp
    else:
        return True,split_exp

def update_disk_variables(expression,done,disk_variables):
    flag, split_exp = check_if_present_done(expression,done)
    if(flag == True):
        t1 = split_exp[1]
        t2 = split_exp[2]
        disk_variables[t1] = int(t2)
    return disk_variables

def update_done(expression,done):
    t1 = expression.split(" ")
    t1 = t1[1]
    done.append(t1)
    return done

def assign_to_disk_variables(variables,t1):
    e_variables = variables[0::2]
    o_values = variables[1::2]
    for j in range(len(e_variables)):
        t1[e_variables[j]] = int(o_values[j])
    return t1

def check_operation(start_checkpoint,end_checkpoint):
    if(start_checkpoint!=-1 and end_checkpoint==-1):
        return 1
    elif(start_checkpoint == -1 and end_checkpoint == -1):
        return 2  
    elif(start_checkpoint!=-1 and end_ckpt_line_no!=-1):
        return 3

def find_start_ckpt_end_ckpt(expression,start_checkpoint,end_checkpoint,cur):
    if(find_indices(expression,'start')):
        start_checkpoint = cur - 3
    if(find_indices(expression, 'end')):
        end_checkpoint = cur - 3
    return start_checkpoint, end_checkpoint

def undo_recovery(start_checkpoint,end_checkpoint,logs, disk_variables):
    if start_checkpoint > end_checkpoint:
        end_checkpoint = -1
    condition = check_operation(start_checkpoint,end_checkpoint)
    if(condition == 1):
        log = logs[start_checkpoint]
        start = log.find("(")+1
        end = log.find(")")
        t1 = log[start:end]
        t2 = t1.replace(" ","")
        t3 = t2.replace(","," ")
        checkpoint_transaction = t3.split(" ")    
        done = []
        log = get_reverse(logs)
        for expression in log: 
            if len(checkpoint_transaction)==0:
                break
            if (check_if_tran(expression)):
                disk_variables = update_disk_variables(expression,done,disk_variables)
            elif (check_commit(expression)):
                done = update_done(expression,done)
            elif (check_start(expression)):
                exp_split = expression.split(" ")
                t1 = exp_split[1]
                flag = False
                for i in checkpoint_transaction:
                    if(i == t1):
                        flag = True
                        break
                if(t1 != enum['ckpt'] and flag == True):               
                    checkpoint_transaction.remove(t1)

    elif(condition == 2):
        logs = get_reverse(logs)
        done = []
        for expression in logs:
            if(check_if_tran(expression)):
                disk_variables = update_disk_variables(expression,done,disk_variables)
            elif(check_commit(expression)):
                done = update_done(expression,done)

    elif(condition == 3):
        start = start_checkpoint + 1
        log = logs[start:]
        log = get_reverse(l)
        done = []
        for expression in log:
            if(check_if_tran(expression)):
                disk_variables = update_disk_variables(expression,done,disk_variables)
            elif(check_commit(expression)):
                done = update_done(expression,done)

    return disk_variables

def main():
    disk_variables = {}
    logs = []
    start_checkpoint = -1
    end_checkpoint = -1
    input_file = sys.argv[1]
    cur = 1
    for expression in open(input_file):
        sp_expression = expression.split()
        s_exp = expression.strip()
        if(cur != 1):
            if(s_exp == ""):
                pass
            else:
                logs.append(expression[1:-2])
                start_checkpoint, end_checkpoint = find_start_ckpt_end_ckpt(expression,start_checkpoint,end_checkpoint,cur)
        elif(cur == 1):
            disk_variables = assign_to_disk_variables(sp_expression,disk_variables)
        cur+=1

    undo_recovery(start_checkpoint,end_checkpoint,logs,disk_variables)
    output_file = open("2019202008_2.txt","w")
    expression = ""
    sorted_d_v = sorted(disk_variables, key=lambda x: len (x[0]))
    for i in sorted_d_v:
        t1 = i + " "
        t2 = t1 + str(disk_variables[i])+" "
        expression = expression + t2
    expression=expression[:-1]
    expression = expression+"\n"
    output_file.write(expression)
    output_file.close()

if(__name__ == "__main__"):
    main()