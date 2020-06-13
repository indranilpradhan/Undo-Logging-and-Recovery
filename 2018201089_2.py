import sys
import re
import operator


def initialise_start():
	return r"^\<START CKPT[ \(]+([a-zA-Z0-9\, ]+)[\)]\>$"
start_ckpt = initialise_start()

def initialise_end():
	return r"^\<END CKPT\>$"
end_ckpt = initialise_end()

def initialise_start():
	return r"^\<START +([a-zA-Z0-9]+)\>$"
start = initialise_start()

def initialise_commit():
	return r"^\<COMMIT +([a-zA-Z0-9]+)\>$"
commit = initialise_commit()

def initialise_val_read():
	return r"^\<([a-zA-Z0-9]+)[\, ]+([a-zA-Z0-9]+)[\, ]+([a-zA-Z0-9]+)\>$"
val_read = initialise_val_read()

parameters=[sys.argv[1]]
i = 0
kv = {}
recoverkv = {}
filename = parameters[0]
f = open(filename,"r")
lines = f.readlines()
key_vals = lines[0].split()


while i+1 <= len(key_vals)-1:
    kv[key_vals[i]] = int(key_vals[i+1])
    i=i+2

transaction_states = {}
if 1:
	end_ckpt_flag = False
i = i+0-i
i = len(lines) - 1

while i >= 1:
	a=re.search(start, lines[i])
	b=re.search(commit, lines[i])
	c=re.search(start_ckpt, lines[i])
	d=re.search(end_ckpt, lines[i])
	e=re.search(val_read, lines[i])


	if a:
		match = re.search(start, lines[i])
	elif b:
		match = re.search(commit, lines[i])
		transaction_states[match.group(1)] = True
	elif c:
		if end_ckpt_flag:
			break
		match = re.search(start_ckpt, lines[i])
	elif d:
		end_ckpt_flag = True
	elif e:
		match = re.search(val_read, lines[i])
		xyz=0
		t_name, var, val = match.group(1), match.group(2), match.group(3)
		abc=0
		if transaction_states.has_key(t_name):
			abc=0
			if not transaction_states[t_name]:
				recoverkv[var] = val
		else:
			xyz=10
			transaction_states[t_name] = False
			recoverkv[var] = val
	i =i- 1

for key in kv:
	if key in recoverkv:
		pass
	else:
		recoverkv[key]=kv[key]

res = ""
li=sorted(recoverkv.keys())
for key in li:
    res =res+ key + " " + str(recoverkv[key]) + " "

temp=res.strip()
print temp