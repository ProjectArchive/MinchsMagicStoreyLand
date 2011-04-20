import os
from Breadboard import *
from BreadboardComponent import *
from Location import *
from Node import *
from Voltage import *
class B2SpiceNew(object):
	
	def __init__(self,board):
		self.board = board
		self.cirName = 'CIRCUIT'+str(id(self))
		#~ getNodeList(self,board)
		try:
			os.system('cd /tmp')
			try:
				os.system('mkdir b2spice')
			except:
				os.system('cd b2spice')
		except:
			raise NameError("I can't find the temp folder!!")
		self.getInputDevices(board)
	#~ e	inputDevices = self.findSource(board)
		#~ rails = self.getRails()	
		
	def getRails(self,board):
		##The 0th value of the list is the bottom of the board
		topRail = board.rails[0]
		midTopRail = board.rails[1]
		midBotRail = board.rails[2]
		botRail = board.rails[3]
		return (topRail,midTopRail,midBotRail,botRail)
		
	def makeRailCards(self,railList):
		railCount = 1;
		railCards = ''
		for item in railList:
			if item != 0:
				railCards += 'V' + str(railCount) + ' 0 ' + str(railCount) + ' dc ' + str(item) + '\n'
				railCount += 1
		return railCards
		
	def getInputDevices(self,board):
		inputDeviceList = []
		for comp in board.componentList:
			if isinstance(comp,InputDevice):
				inputDeviceList.append(comp)
		self.inputDeviceList = inputDeviceList
		return inputDeviceList
	
	def makeInputDeviceCards(self,board):
		inputDeviceCards = ''
		inputDeviceList = self.inputDeviceList
		for item in inputDeviceList:
			if item.voltageType == 'AC':
				inputDeviceCards += 'V' + str(id(item)) + ' ' + str(item.pinList[0].Node.number) + ' 0 ' + 'sin \n'
			else:
				inputDeviceCards += 'V' + str(id(item)) + ' ' + str(item.pinList[0].Node.number) + ' 0 ' + 'dc ' + str(item.voltage.volts) + ' \n'
		return inputDeviceCards

	def makeAnalysisCards(self,board,analysisType,scopedNode,vMin=0,vMax=0,stepSize=0,tstep=0,ttotal=0,stepType='lin',numSteps=0,startFreq=0,endFreq=0):
		if analysisType != 'dc' or 'ac' or 'tran':
			raise NameError("I don't know how to analyze this!")
		if analysisType == 'ac':
			return self.makeACCards(board,scopedNode,stepType,numSteps,startFreq,endFreq)
		#~ elif analysisType == 'dc':
			#~ return self.makeDCCards(
		
	def makeACCards(self,board,node,stepType,numSteps,startFreq,endFreq):
		acLine = '.ac %s %g %g %g \n' % stepType,numSteps,startFreq,endFreq
		printLine = 'print ac v(%g) \n' % node
		return acLine + printLine
	
	def clearEmptyNodes(self):
		"""notes how many times a node appears in a circuit.
		if it's only one, and not power, then we take action and remove it"""
		d={}
		for component in self.board.componentList:
			if not isinstance(component,FixedBreadboardComponent):
				for pin in component.pinList:
					d[pin.Node.number]=d.get(pin.Node.number,0)+1
		for val in d:
			if d[val]==1 and val!=1 and val!=2 and val!=3 and val!=0:
				count=-1
				for component in self.board.componentList:
					count+=1
					for pin in component.pinList:
						if pin.Node.number == val:
							del self.board.componentList[count]
		return d
	
		
	def getNodeList(self,board):
		"""Creates a list of all 
		occupied nodes on a breadboard"""
		nodeList = []
		for comp in self.board.componentList:
			for pin in comp.pinList:
				nodeList.append(pin.Node.node)
		self.nodeList = nodeList
		
	def getNodes(self,component):
		"""returns a string that contains
		the nodes of a component, separated by spaces"""
		nodeStr = ' '
		for pins in component.pinList:
			nodeStr += str(pins.Node.node) + ' '
		return nodeStr
				
		
if __name__ == '__main__':
	bb = Breadboard()
	Vsource = InputDevice(10,'AC',60)
	V2 = InputDevice(10)
	bb.putComponent(Vsource,30,5)
	bb.putComponent(V2,30,5)
	b = B2SpiceNew(bb)
	print b.makeInputDeviceCards(bb)
	print b.makeRailCards(bb.rails)	
