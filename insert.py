data = "insert (momey=400) into users / (username=tomas)"

data = data.replace(', ', ',')
data = data.replace(';', '')
data = data.split(' ')

args = data[1]
args2 = data[5]
data = data[3]
args = args.replace('(', '')
args = args.replace(')', '')
args2 = args2.replace('(', '')
args2 = args2.replace(')', '')

arguments_arg = {}
if len(args.split('=')) == 2:
	temp = args.split('=')
	arguments_arg[temp[0]] = temp[1]
else:
	for arg in args:
		temp = arg.split('=')
		arguments_arg[temp[0]] = temp[1]

arguments = {}
if len(args2.split('=')) == 2:
	temp = args2.split('=')
	arguments[temp[0]] = temp[1]
else:
	for arg in args2:
		temp = arg.split('=')
		arguments[temp[0]] = temp[1]

temp_args = []
rows = open("/home/s3w3n/Documents/DB/" + str(data), "r").readlines()
temp_args = rows[0].replace('\n', '')
temp_args = temp_args.split(' ')


index = 0
for arg in temp_args:
	if arg == list(arguments.keys())[0]:
		break
	index += 1

value = arguments[list(arguments.keys())[0]]

temp = ""
for arg in args:
	i = 0
	rows = open("/home/s3w3n/Documents/DB/" + str(data), "r").readlines()
	for col in rows[0].split(' '):
		if arg in col:
			break
		i += 1

	rows.pop(0)
	
	rows_temp = []
	rows_temp_index = []

	a = 0
	for row in rows:
		row = row.replace('\n', '')
		cols = row.split()
		if cols[index] == value:
			rows_temp.append(row)
			rows_temp_index.append(a+1)
		a += 1

lines = []
i -= 1
value_arg = arguments_arg[list(arguments_arg.keys())[0]]
for row in rows_temp:
	cols = row.split(' ')
	if len(cols) > i + 2:
		cols[i] = value_arg + ","
	else:
		cols[i] = value_arg
	lines.append(' '.join(cols))


a = 0 
for index in rows_temp_index:
	replace_line("/home/s3w3n/Documents/DB/" + str(data), index, lines[a]+"\n")
	a += 1
#return "succes"	