arguments = {'id': 1, 'location': 'Ostrava'}
rows = open('tst', 'r').readlines()
newfile = rows
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

f = open('tst', 'w')
for line in newfile:
	f.write(line)
