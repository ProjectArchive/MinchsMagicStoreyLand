import os
from Breadboard import *
from BreadboardComponent import *
from Location import *
from Node import *
from Voltage import *

class B2Spice(object):
	"""encapsulatstes a set of methods to
	turn BreadBoard Components into a netlist
	line usable by SPICE. Also contains anaylsis
	options and the interface with SPICE"""
	def __init__(self,board):
		self.board = board
		self.cirName = 'CIRCUIT'+str(id(self))
		self.nodeList = self.makeNodeList()
		self.netList = self.buildNetList()
		try:
			os.system('mkdir .temp')
			os.system('cd .temp')
		except:
			pass
	
	def makeNodeList(self):
		board = self.board
		nodeList = []
		for comp in board.componentList:
			for pin in comp.pinList:
				nodeList.append(pin.Node.node)
		return nodeList
	
	def getNodes(self,component):
		nodeStr = ' '
		for pins in component.pinList:
			nodeStr += str(pins.Node.node) + ' '
		return nodeStr
		
	def getAttr(self,component):
		attributeDict = component.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		attrKey = attrKey[0] + str(id(component))
		return str(attrKey),str(attrVal)
		
	def buildText(self,component):
		if isinstance(component,Capacitor):
			suffix = ' ic=0'
		else:
			suffix = ''
		nodes = self.getNodes(component)
		attr = self.getAttr(component)
		ans = attr[0] + nodes + attr[1] + suffix
		return ans
	
	def getRail(self):
		board = self.board
		compList = board.componentList
		for comp in compList:
			for pin in comp.pinList:
				if pin.Node.node < 4 and pin.Node.node >0:
					if pin.Node.node ==1:
						voltagePower = 2.5
					elif pin.Node.node ==2:
						voltagePower = 2.5
					elif pin.Node.node ==3:
						voltagePower = 5
					else:
						voltagePower = 0
					voltageNode = pin.Node.node
					return voltagePower,voltageNode
				else:
					voltagePower = 0
					voltageNode = 0
					return voltagePower,voltageNode
		
	def getRailandAnalysis(self):
		board = self.board
		vPower,vNode = self.getRail()
		sourceName = 'v' + str(id(board))
		groundNode =  '0'
		powerNode = str(vNode)
		power = str(vPower)
		sourceLine = sourceName + ' ' + groundNode + ' ' + powerNode + ' dc ' + power
		analysisLine = '.dc ' + sourceName + ' ' + power + ' ' + power + ' 1'
		return sourceLine,analysisLine
		
	def buildNetList(self):
		board = self.board
		netList = self.cirName + '\n'
		sourceLine,analysisLine = self.getRailandAnalysis()
		netList += sourceLine + '\n'
		compList = board.componentList
		for components in compList:
			netList += self.buildText(components) + '\n'
		netList += analysisLine + '\n'
		vAtNodeLine = '.print dc'
		for node in self.nodeList:
			if int(node) < 1:
				vAtNodeLine += ''
			else:
				vAtNodeLine += ' v(%s)' % node
		vAtNodeLine += ' \n'
		netList += vAtNodeLine
		netList += '.end'
		return netList
	
	def parse(self,textFile):
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
					if type(a) != int:
						a='0'
					if 'sw' in a or a=='':
<<<<<<< HEAD
						a = 2**8
=======
						a = 12345
>>>>>>> 51b4357e1eb66bf5d37c46ea884251438eddbdf6
					key.append(int(a)) 
				if b[i][j:j+2] == ('e+' or 'e-'):
					val.append(float(b[i][j-8:j+4]))
		a = zip(key,val)
		for part in a:
<<<<<<< HEAD
			if part[0]==2**8:
=======
			if part[0]==12345:
>>>>>>> 51b4357e1eb66bf5d37c46ea884251438eddbdf6
				a.remove(part)
		return dict(a)
			
		
	def loadBb(self):
		board = self.board
		fileName = self.cirName + '.cir'
		resFileName = 'res.txt'
		netList = self.netList
		os.system('touch %s' % fileName) 
		os.system('touch %s' % resFileName)
		fout = open(fileName,'w')
		fout.write(netList)
		fout.close()
		res = os.system('ngspice -b ' + fileName + ' > ' + resFileName) 
		#~ res = os.system('ngspice -b ' + fileName)
		fin = open(resFileName,'r')
		voltageNodeDict = self.parse(fin)
		fin.close()
		os.system('rm ' + fileName)
		os.system('rm ' + resFileName)
		os.system('cd ..')
		os.system('rm -rf .temp/')
		return voltageNodeDict
		#~ return fin
	
	#~ def getVoltageAtLocations(self,board):
		#~ nodeList = []
		#~ for comp in board.componentList:
			#~ for loc in comp.pinList:
				#~ nodeList += 
	

if __name__ == "__main__":
	bb = Breadboard()
	r1 = Resistor(500)
	w2 = Wire()
	r3 = Resistor(2000)
	#~ c1 = Capacitor(.000001)
	r4 = Resistor(100000)
	r5 = Resistor(200)
	#~ w1 = Wire()
	bb.putComponent(r1,18,1,18,7)
	bb.putComponent(w2,18,6,11,6)
	bb.putComponent(r3,18,5,22,5)
	bb.putComponent(r4,22,6,22,17)
	bb.putComponent(r5,11,5,11,17)
	r1.pinList[0].Node.voltage = Voltage(-5)
	b = B2Spice(bb)
<<<<<<< HEAD
	print b.buildNetList()
=======
	#~ print b.buildNetList()
>>>>>>> 9044585fa7f5581b61a55cebd433321b3e611281
	print b.loadBb()
