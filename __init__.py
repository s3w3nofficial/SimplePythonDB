import socket, os.path

def startServer():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	s.bind(("127.0.0.1",5901))
	s.listen(1)	

	while True:

        	connect, address = s.accept()

		resp = (connect.recv(1024)).strip()
		#print str(resp) + " " + str(address)
        	dbHandler(resp)
		#connect.send("You said '" + resp + "' to me\n")

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
			for arg in args:
				table.write(arg + " ")
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
			args = rows[0].split(' ')
			args.pop()

		for arg in args:
			i = 0
			rows = open("/home/s3w3n/Documents/DB/" + str(data), "r").readlines()
			for col in rows[0].split(' '):
				if arg in col:
					break
				i += 1
			temp = ""
			rows.pop(0)
			for row in rows:
				cols = row.split(' ')
				temp += cols[i].replace('\n', '') + " "
			print temp
	else:
		return "table doesnt exist"

def insertData(data):
	if tableExist(data[3]) == True:
		args = data[1]
		data = data[3]
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

		print arguments


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

	if data != "":
		data = data.replace(', ', ',')
		data = data.replace(';', '')
		data = data.split(' ')
		if len(data) == 4: #create table
			if data[0] == "create":
				if data[1] == "table":
					createTable(data)
			elif data[0] == "select":
				if data[2] == "from":
					selectData(data)
			elif data[0] == "insert":
				if data[2] == "into":
					insertData(data)
			else:
				return "invalid commands"
	else:
		return "value error"

if __name__ == "__main__":
	startServer()
