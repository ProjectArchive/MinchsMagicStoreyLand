def parse(textFile):
	"""ugliest fucking code ever.
	Loops through, looking for v(x).
	makes that v(x) into a list.
	Then looks for e+ or e-, making that into a list.
	euqal numbers of e's and v(x)s.
	zips both into a combined list.
	kills the voltage at the source nodes.
	converts shortened list to dictionary.
	bye bye.
	"""
	
	key=[]
	val=[]
	b=[]
	flag=0

	for line in textFile:
		b.append(line)
	for i in range(len(b)-1):
		for j in range(len(b[i])-1):
			if b[i][j:j+2] == 'v(' or b[i][j:j+2] == 'v-':
				for k in range(-1,5):
					if b[i][j+k]==')':
						flag=k
				a = b[i][j+2:j+flag]
				if 'sw' in a or a=='':
					a = 'V-source'
				key.append(a) # = b[i+2][j-22:j-10]
			if b[i][j:j+2] == ('e+' or 'e-'):
				val.append(b[i][j-8:j+4])
	a = zip(key,val)
	for part in a:
		if part[0]=='V-source':
			a.remove(part)
	return dict(a)

