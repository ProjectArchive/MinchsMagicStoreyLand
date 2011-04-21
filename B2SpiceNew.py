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
		os.system('mkdir b2spice')
		os.system('cd b2spice')
		self.clearEmptyNodes()
		self.getInputDevices()
		self.rails = self.getRails()
		self.InputDeviceList = self.getInputDevices()
		self.nodeList = self.getNodeList()
		
		
	def getRails(self):
		##The 0th value of the list is the bottom of the board
		topRail = self.board.rails[0]
		midTopRail = self.board.rails[1]
		midBotRail = self.board.rails[2]
		botRail = self.board.rails[3]
		return (topRail,midTopRail,midBotRail,botRail)
		
	def makeRailCards(self):
		railCount = 1;
		railCards = ''
		for item in self.rails:
			if item != 0:
				railCards += 'V%g %g 0 dc %g \n' % railCount,railCount,item
				#~ railCards += 'V' + str(railCount) + ' 0 ' + str(railCount) + ' dc ' + str(item) + '\n'
				railCount += 1
		return railCards
		
	def getInputDevices(self):
		inputDeviceList = []
		for comp in self.board.componentList:
			if isinstance(comp,InputDevice):
				inputDeviceList.append(comp)
		return inputDeviceList
	
	def makeInputDeviceCards(self):
		inputDeviceCards = ''
		for item in self.inputDeviceList:
			if item.voltageType == 'AC':
				inputDeviceCards += 'V%g %g 0 sin \n' % id(item),item.pinList[0].Node.number
				#~ inputDeviceCards += 'V' + str(id(item)) + ' ' + str(item.pinList[0].Node.number) + ' 0 ' + 'sin \n'
			else:
				inputDeviceCards += 'V%g %g 0 dc %g \n' % id(item),item.pinList[0].Node.number,item.voltage.volts
				#~ inputDeviceCards += 'V' + str(id(item)) + ' ' + str(item.pinList[0].Node.number) + ' 0 ' + 'dc ' + str(item.voltage.volts) + ' \n'
		return inputDeviceCards

	def makeAnalysisCards(self,analysisType,scopedNode,vMin=0,vMax=0,stepSize=0,tstep=0,ttotal=0,stepType='lin',numSteps=0,startFreq=0,endFreq=0):
		if analysisType != 'dc' or 'ac' or 'tran':
			raise NameError("I don't know how to analyze this!")
		if analysisType == 'ac':
			return self.makeACCards(scopedNode,stepType,numSteps,startFreq,endFreq)
		elif analysisType == 'dc':
			return self.makeDCCards(scopedNode,vMin,vMax,stepSize)
		else:
			return self.makeTranCards(scopedNode,tstep,ttotal)
		
	def makeACCards(self,scopedNode,stepType,numSteps,startFreq,endFreq):
		if len(InputDeviceList) <1:
			raise NameError('There are no input devices...')
		acLine = '.ac %s %g %g %g \n' % stepType,numSteps,startFreq,endFreq
		printLine = '.print ac v(%g) \n' % scopedNode
		return acLine + printLine
	
	def makeDCCards(self,scopedNode,vMin,vMax,stepSize):
		dcInputDeviceList = []
		for item in self.inputDeviceList:
			if item.voltageType == 'DC':
				dcInputDeviceList.append(item)
		self.dcInputDeviceList = dcInputDeviceList
		if len(dcInputDeviceList) or len(InputDeviceList) <1:
			raise NameError("There's nothing for me to analyze!")
		inp = dcInputDeviceList[0]
		dcLine = '.dc V(%g) %g %g %g \n' % id(inp),vMin,vMax,stepSize
		printLine = '.print dc v(%g) \n' % scopedNode 
		return acLine+printLine
	
	def makeTranCards(scopedNode,tstep,ttotal):
		tranLine = '.tran %g %g \n' % tstep, ttotal
		printLine = '.print tran v(%g) \n' % scopedNode
		return tranLine+printLine
	
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
	
		
	def getNodeList(self):
		"""Creates a list of all 
		occupied nodes on a breadboard"""
		nodeList = []
		for comp in self.board.componentList:
			for pin in comp.pinList:
				nodeList.append(pin.Node.number)
		return nodeList
		
	def getNodes(self,component):
		"""returns a string that contains
		the nodes of a component, separated by spaces"""
		nodeStr = ' '
		for pins in component.pinList:
			nodeStr += str(pins.Node.number) + ' '
		return nodeStr
				
		
if __name__ == '__main__':
	bb = Breadboard()
	Vsource = InputDevice(10,'AC',60)
	V2 = InputDevice(10)
	bb.putComponent(Vsource,30,5)
	bb.putComponent(V2,30,5)
	b = B2SpiceNew(bb)
	

