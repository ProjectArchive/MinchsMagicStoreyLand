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
		self.nodeList = self.makeNodeList(board)
		self.netList = self.buildNetList(board)
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
					voltagePower = pin.Node.voltage.volts
					voltageNode = pin.Node.node
					return voltagePower,voltageNode
				else:
					voltagePower = 0
					voltageNode = 0
					return voltagePower,voltageNode
		
	def getRailandAnalysis(self):
		board = self.board
		vPower,vNode = self.getRail(board)
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
		sourceLine,analysisLine = self.getRailandAnalysis(board)
		netList += sourceLine + '\n'
		compList = board.componentList
		for components in compList:
			netList += self.buildText(components) + '\n'
		netList += analysisLine + '\n'
		vAtNodeLine = '.print dc'
		for node in self.nodeList:
			vAtNodeLine += ' v(%s)' % node
		vAtNodeLine += ' \n'
		netList += vAtNodeLine
		netList += '.end'
		return netList
			
		
	def loadBb(self):
		board = self.board
		fileName = self.cirName + '.cir'
		resFileName = 'res.txt'
		netList = self.netList
		os.system('touch %s' % fileName) 
		fout = open(fileName,'w')
		fout.write(netList)
		fout.close()
		res = os.system('ngspice -b ' + fileName + ' > ' + resFileName) 
		os.system('rm ' + fileName)
		os.system('cd ..')
		os.system('rm -rf .temp/')
		return res
	
	#~ def getVoltageAtLocations(self,board):
		#~ nodeList = []
		#~ for comp in board.componentList:
			#~ for loc in comp.pinList:
				#~ nodeList += 


	def railExists(self,board):
		compList = board.componentList
		nodeList = []
		for comp in compList:
			for pin in comp.pinList:
				nodeList.append(pin.Node.node)
		for node in nodeList:
			if node > 0 and node < 5:
				return True
		return False
	


bb = Breadboard()
r1 = Resistor(500)
w2 = Wire()
r3 = Resistor(2000)
#~ c1 = Capacitor(.000001)
c4 = Capacitor(.00001)
r5 = Resistor(200)
#~ w1 = Wire()
bb.putComponent(r1,18,1,18,7)
bb.putComponent(w2,18,6,11,6)
bb.putComponent(r3,18,5,22,5)
bb.putComponent(c4,22,6,22,17)
bb.putComponent(r5,11,5,11,17)
r1.pinList[0].Node.voltage = Voltage(-5)
b = B2Spice(bb)
#~ print b.buildNetList(bb)
b.loadBb(bb)
