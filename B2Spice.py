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
		self.clearEmptyNodes()
		self.cirName = 'CIRCUIT'+str(id(self))
		self.nodeList = self.makeNodeList()
		self.netList = self.buildNetList()
		try:
			os.system('mkdir .temp')
			os.system('cd .temp')
		except:
			pass
	
	def clearEmptyNodes(self):
		"""notes how many times a node appears in a circuit.
		if it's only one, and not power, then we take action and remove it"""
		d={}
		for component in self.board.componentList:
			if not isinstance(component,FixedBreadboardComponent):
				for pin in component.pinList:
					d[pin.Node.number]=d.get(pin.Node.number,0)+1
		for val in d:
			if d[val]==1 and (val!=1 and val!=2 and val!=3 and val!=0):
				count=-1
				for component in self.board.componentList:
					count+=1
					for pin in component.pinList:
						if pin.Node.number == val:
							del self.board.componentList[count]
		return d
			
	
	def makeNodeList(self):
		"""Creates a list of all 
		occupied nodes on a breadboard"""
		board = self.board
		nodeList = []
		for comp in board.componentList:
			for pin in comp.pinList:
				nodeList.append(pin.Node.number)
		return nodeList
	
	def getNodes(self,component):
		"""returns a string that contains
		the nodes of a component, separated by spaces.
		"""
		nodeStr = ' '
		for pins in component.pinList:
			nodeStr += str(pins.Node.number) + ' '
		return nodeStr
		
	def getAttr(self,component):
		"""returns a tuple containing the attribute
		of the component and its value,
		both as strings"""
		attributeDict = component.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		attrKey = attrKey[0] + str(id(component))
		return str(attrKey),str(attrVal)
		
	def buildText(self,component):
		"""builds the line of text that SPICE
		uses to describe the component. Only 
		takes Resistors, Wires, and Capacitors 
		right now. Also sets initial conditions
		for Capacitors."""
		if isinstance(component,Capacitor):
			suffix = ' ic=0'
		else:
			suffix = ''
		nodes = self.getNodes(component)
		attr = self.getAttr(component)
		ans = attr[0] + nodes + attr[1] + suffix
		return ans
	
	def getRail(self):
		"""finds the voltage on the rail
		of the breadboard. returns the Node
		and power of the voltage rail source"""
		board = self.board
		compList = board.componentList
		for comp in compList:
			for pin in comp.pinList:
				if pin.Node.number < 4 and pin.Node.number >0:
					if pin.Node.number ==1:
						voltagePower = 2.5
					elif pin.Node.number ==2:
						voltagePower = 2.5
					elif pin.Node.number ==3:
						voltagePower = 5
					else:
						voltagePower = 0
					voltageNode = pin.Node.number
					return voltagePower,voltageNode
				else:
					voltagePower = 0
					voltageNode = 0
					return voltagePower,voltageNode
		
	def getRailandAnalysis(self):
		"""builds the line that describes
		the source voltage of the breadboard
		(probably from the rail). In addition, this method
		tells SPICE what kind of analysis to do on the circuit.
		Only handles DC circuits right now."""
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
		"""This is the demi-motherlode. This
		builds a string that describes the circuit and 
		type of analysis. Only handles DC circuits right now
		"""
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
	
		
	
	#~ def parse(self,textFile):
		#~ key=[]
		#~ val=[]
		#~ b=[]
		#~ flag=0
#~ 
		#~ for line in textFile:
			#~ b.append(line)
			#~ print line,
		#~ for i in range(len(b)-1):
			#~ for j in range(len(b[i])-1):
				#~ if b[i][j:j+2] == 'v(' or b[i][j:j+2] == 'v-':
					#~ for k in range(-1,5):
						#~ if b[i][j+k]==')':
							#~ flag=k
					#~ a = b[i][j+2:j+flag]
					#~ if 'sw' in a or a=='':
						#~ a = 'Power'
					#~ key.append(a) 
				#~ if b[i][j:j+2] == 'e+' or  b[i][j:j+2]=='e-':
					#~ val.append(float(b[i][j-8:j+4]))
		#~ a = zip(key,val)
		#~ return dict(a)
		
	def parse(self,textFile): 
		"""parses the output string from SPICE.
		Not perfect, probably not going to be used
		later."""
		b=[]
		for line in textFile:
			b.append(line)
		for i in range(len(b)-1):
			if 'Index' in b[i]:
				print b[i],b[i+1],b[i+2]
		return True
			
		
	def loadBb(self):
		"""Creates the temporary files and directories
		necessary for circuit analysis. Initializes ngspice, feeds
		the netlist to it, and parses the output. Deletes all the files
		and directories after analysis. Cory's really into anal.
		"""
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
	c1 = Capacitor(.000001)
	r4 = Resistor(1000)
	r5 = Resistor(200)
	w1 = Wire()
	bb.putComponent(r1,18,1,18,7)
	bb.putComponent(w2,18,6,11,17)
	bb.putComponent(r3,18,5,11,17)
	bb.putComponent(c1,22,6,22,17)
	bb.putComponent(w1,11,5,11,17)
	r1.pinList[0].Node.voltage = Voltage(-5)
	b = B2Spice(bb)
	b.clearEmptyNodes()
	print b.buildNetList()
	print b.loadBb()
