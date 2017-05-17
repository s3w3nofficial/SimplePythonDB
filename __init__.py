import socket, os.path
from threading import Thread

def startServer():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	s.bind(("127.0.0.1",5901))
	s.listen(5)	

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

		rows = []
		with open("/home/s3w3n/Documents/DB/" + str(data), "r") as table:
			for row in table:
				rows.append(row)
			hedding = rows[0].split(' ')
			idx = []
			i = 0
			for h in hedding:
				for arg in args:
					if arg in h:
						idx.append(i)	
				i += 1
			rows.pop(0)
			r = []
			res = []
			for row in rows:
				r = row.split(' ')
				res.append(r)
			for tmp in res:
				for i in idx:
					print tmp[i]
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
		data = data.split(' ')
		if len(data) == 4: #create table
			if data[0] == "create":
				if data[1] == "table":
					createTable(data)
			elif data[0] == "select":
				if data[2] == "from":
					selectData(data)
	else:
		return "value error"

if __name__ == "__main__":
	Thread(target=startServer).start()
