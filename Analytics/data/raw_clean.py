filenames = [ '03-2014-aps.txt' ]

for filename in filenames:
	f = open(filename, 'r')

	contents = f.readlines()

	for line in contents:
		if line[0] == '{':
			print line