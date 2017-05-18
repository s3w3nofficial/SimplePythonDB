import socket, os.path, os
import signal
import sys
def signal_handler(signal, frame):
	print('Ctrl+C')
	os.system('rm /home/spdb/run.pid')
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

pidf = open('/home/spdb/run.pid', 'w')
pidf.write(str(os.getpid()))
pidf.close()

def startServer():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	s.bind(("127.0.0.1",5901))
	s.listen(1)

	while True:

        	connect, address = s.accept()

		resp = (connect.recv(1024)).strip()
		#print str(resp) + " " + str(address)
        	resp = dbHandler(resp)
		connect.send(resp)

        	connect.close()

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def createTable(data):
	if tableExist(data[2]) == False:
		args = data[-1]
		data.pop(-1)
		args = args.replace('(', '')
		args = args.replace(')', '')

		if ',' in args:
			args = args.split(',')
		else:
			args = [args]

		with open("/home/spdb/DB" + str(data[2]), "w+") as table:
			i = 0
			for arg in args:
				if len(args) - 1 != i:
					table.write(arg + " ")
				else:
					table.write(arg)
				i += 1
		return "success"
	else:
		return "table already exist"

def selectData(data):
	if tableExist(data[3]) == True:
		args = data[1]
		data = data[3]
		args = args.replace('(', '')
		args = args.replace(')', '')

		if ',' in args:
			args = args.split(',')
		else:
			args = [args]

		if args[0] == '*':
			rows = open("/home/spdb/DB" + str(data), "r").readlines()
			args = rows[0].replace('\n', '')
			args = args.split(' ')

		temp = ""
		for arg in args:
			i = 0
			rows = open("/home/spdb/DB" + str(data), "r").readlines()
			for col in rows[0].split(' '):
				if arg in col:
					break
				i += 1

			rows.pop(0)
			a = 0
			for row in rows:
				cols = row.split(' ')
				if len(rows) > a + 1:
					temp += cols[i].replace('\n', '') + ","
				else:
					temp += cols[i].replace('\n', '')
				a += 1
			temp += " "
		print temp
		return temp
	else:
		return "table doesnt exist"

def selectDataFiltered(data):
	args = data[1]
	args2 = data[5]
	data = data[3]
	args = args.replace('(', '')
	args = args.replace(')', '')
	args2 = args2.replace('(', '')
	args2 = args2.replace(')', '')

	if ',' in args:
		args = args.split(',')
	else:
		args = [args]

	arguments = {}
	if len(args2.split('=')) == 2:
		temp = args2.split('=')
		arguments[temp[0]] = temp[1]
	else:
		for arg in args2:
			temp = arg.split('=')
			arguments[temp[0]] = temp[1]

	temp_args = []
	rows = open("/home/spdb/DB" + str(data), "r").readlines()
	temp_args = rows[0].replace('\n', '')
	temp_args = temp_args.split(' ')


	index = 0
	for arg in temp_args:
		if arg == list(arguments.keys())[0]:
			break
		index += 1

	value = arguments[list(arguments.keys())[0]]

	if args[0] == '*':
		rows = open("/home/spdb/DB" + str(data), "r").readlines()
		args = rows[0].replace('\n', '')
		args = args.split(' ')

	temp = ""
	for arg in args:
		i = 0
		rows = open("/home/spdb/DB" + str(data), "r").readlines()
		for col in rows[0].split(' '):
			if arg in col:
				break
			i += 1

		rows.pop(0)
		
		rows_temp = []
		a = 0
		for row in rows:
			cols = row.split()
			if cols[index] == value:
				rows_temp.append(row)
			a += 1

		a = 0
		for row in rows_temp:
			cols = row.split(' ')
			if len(rows_temp) > a + 1:
				temp += cols[i].replace('\n', '') + ","
			else:
				temp += cols[i].replace('\n', '')
			a += 1
		temp += " "
	print temp
	return temp;

def insertData(data):
	if tableExist(data[3]) == True:
		args = data[1]
		table = data[3]
		args = args.replace('(', '')
		args = args.replace(')', '')

		if ',' in args:
			args = args.split(',')
		else:
			args = [args]

		i = 0
		arguments = {}
		for arg in args:
			temp = arg.split('=')
			arguments[temp[0]] = temp[1]

		rows = open("/home/spdb/DB" + table, 'r').readlines()
		newfile = rows
		for fil in newfile:
			for fi in fil:
				fi.replace('\n', '') 
		toAdd = ''
		for header in rows[0].replace('\n', '').split(' '):
			value = 'NULL'
			if header in arguments:
				value = arguments[header]
			if toAdd == '':
				toAdd = str(value)
			else:
				toAdd += ' ' + str(value)

		newfile += '\n' + toAdd

		f = open("/home/spdb/DB" + table, 'w')
		for line in newfile:
			f.write(line)

		return "success"
	else:
		return "table doesnt exist"

def insertIntoFiltered(data):
	if tableExist(data[3]) == True:
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
		rows = open("/home/spdb/DB" + str(data), "r").readlines()
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
			rows = open("/home/spdb/DB" + str(data), "r").readlines()
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
			replace_line("/home/spdb/DB" + str(data), index, lines[a]+"\n")
			a += 1
		return "success"	
	else:
		return "table doesnt exist"

def dropTable(tablename):
	if tablename == "all" or tablename == "*":
		for root, dirs, files in os.walk("/home/spdb/DB"):
			for f in files:
				filename = os.path.join(root, f)
	 			os.remove(filename)
		return "success"
	elif tableExist(data) == True:	
		os.remove("/home/spdb/DB" + str(tablename))
		return "success"
	else:
		return "table doesnt exist"

def tableExist(name):
	tmp = os.path.exists("/home/spdb/DB" + str(name))
	return tmp

def dbHandler(data):

	#commands
	"""
	create table tablename (param,param)
	select (param,param) from tablename
	insert (col=param,col=param) into tablename
	drop param = [all,*,tablename]
	"""
	msg = ""	

	if data != "":
		data = data.replace(', ', ',')
		data = data.replace(';', '')
		data = data.split(' ')
		if len(data) == 6:
			if data[0] == "select":
					if data[2] == "from":
						if data[4] == "/":
							msg = selectDataFiltered(data)
			elif data[0] == "insert":
					if data[2] == "into":
						if data[4] == "/":
							msg = insertIntoFiltered(data)
 		elif len(data) == 4: #create table
			if data[0] == "create":
				if data[1] == "table":
					msg = createTable(data)
			elif data[0] == "select":
				if data[2] == "from":
					msg = selectData(data)
			elif data[0] == "insert":
				if data[2] == "into":
					msg = insertData(data)
			else:
				msg = "invalid commands"
		elif len(data) == 2:
			if data[0] == "drop":
				msg = dropTable(data[1])
			else:
				msg = "invalid commands"
	else:
		msg = "value error"

	return msg

if __name__ == "__main__":
	startServer()
