import socket, os.path

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

		with open("/home/s3w3n/Documents/DB/" + str(data[2]), "w+") as table:
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
			rows = open("/home/s3w3n/Documents/DB/" + str(data), "r").readlines()
			args = rows[0].replace('\n', '')
			args = args.split(' ')

		temp = ""
		for arg in args:
			i = 0
			rows = open("/home/s3w3n/Documents/DB/" + str(data), "r").readlines()
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

		rows = open("/home/s3w3n/Documents/DB/" + table, 'r').readlines()
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

		f = open("/home/s3w3n/Documents/DB/" + table, 'w')
		for line in newfile:
			f.write(line)

		return "success"
	else:
		return "table doesnt exist"

def tableExist(name):
	tmp = os.path.exists("/home/s3w3n/Documents/DB/" + str(name))
	return tmp

def dbHandler(data):

	#commands
	"""
	create table tablename (param,param)
	select (param,param) from tablename
	insert (col=param,col=param) into tablename
	"""
	msg = ""	

	if data != "":
		data = data.replace(', ', ',')
		data = data.replace(';', '')
		data = data.split(' ')
		if len(data) == 4: #create table
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
	else:
		msg = "value error"

	return msg

if __name__ == "__main__":
	startServer()
