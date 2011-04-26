def input_parser():
	
	# initialize a bunch of storage arrays

	vals =[] #list of list
	# open the file
	fout = open('sampleCircuitData.txt')
	content_string = ""
	start = False
	lineNum = 0
	
	n = 11
	lineNum = 0
	
	for i in range(n):
		vals.append([])
		
	for line in fout:
		if not start and line.find('Values') != -1:
			start = True
			continue
		if start:
			if line[0] != '\t':
				line = line[line.find('\t'):]
			line = line.translate(None,'\t')
			print line
			vals[lineNum%n].append(float(line))
			lineNum +=1
	return vals
	
	
input_parser()

