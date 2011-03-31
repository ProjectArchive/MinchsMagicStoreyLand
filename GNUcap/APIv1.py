##Version 1 of the Python-GNUcap API (I'm calling it Pcap). This script will build a circuit file in GNUcap using Python.
import os
fileExtension = '.ckt'
fileName = 'c1%s' % fileExtension
os.system('touch %s' % fileName) 
fout = open('c1.ckt','w')
title = 'VOLTAGE DIVIDER'
circuit= ['Vsupply 0 1 DC 1','R1 2 1 1.k','R2 0 2 1.k','R3 0 2 1.k']
cmdList = ['.print dc i(R1) i(R2) i(R3) ','.dc','.end']



fout.write('%s\n' % title) 
for line in circuit:
	fout.write('%s\n' % line) 

for line in cmdList:
	fout.write('%s\n' % line) 

fout.close()

s = os.popen('gnucap -b %s' % fileName)
result = s.read()
status = s.close()
os.system('rm c1.ckt')
print result


