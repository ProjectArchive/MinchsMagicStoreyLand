import os
from Breadboard import *
from BreadboardComponent import *
from Location import *

class B2Spice(object):
	"""encapsulatst4es a set of methods to
	turn BreadBoard Components into a netlist
	line usable by SPICE. Also contains anaylsis
	options and the interface with SPICE"""
	def __init__(self):
		self.width = 63
		self.height = 18
	
	def getNodes(self,BreadboardComponent):
		nodeStr = ' '
		for pins in BreadboardComponent.pinList:
			nodeStr += str(pins.node) + ' '
		return nodeStr
		
	def getAttr(self,BreadboardComponent):
		attributeDict = BreadboardComponent.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		return str(attrKey[0]),str(attrVal)
		
	def buildText(self,BreadboardComponent):
		nodes = self.getNodes(BreadboardComponent)
		attr = self.getAttr(BreadboardComponent)
		ans = attr[0] + nodes + attr[1]
		return ans
		
	def buildNetList(self,Breadboard):
		netList = ''
		compList = Breadboard.componentList
		for components in compList:
			netList += self.buildText(components) + '\n'
		return netList
		
	def talkToSpice(self,Breadboard):
		fileExtension = '.cir'
		fileName = 'c1%s' % fileExtension
		os.system('touch %s' % fileName) 
		fout = open(fileName,'w')
		title = 'C1'
		fout.write('%s\n' % title) 
		fout.write(B2Spice.buildNetList(Breadboard))
		cmdList = ['.print dc i(R1) i(R2) i(R3) ','.dc','.end']
		fout.close()

		s = os.popen('ngspice -b %s' % fileName)
		result = s.read()
		status = s.close()
		os.system('rm fileName')
		return result

		
	
	def __repr__(self):
		return 'at least something worked'
