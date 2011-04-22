#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *
import math
import copy


class BreadboardPanel(wx.Panel):
	PLAINWIRE = "plainwire"
	def __init__(self, parent,breadboard,buttonManager=None, *args, **kwargs):
 		wx.Panel.__init__(self, parent,size=(945,270),*args,**kwargs)
 		self.parent = parent
		self.breadboard = breadboard
		self.buttonManager = buttonManager

		self.emptyImage = wx.Image('res/blank_slot.png')
		print self.emptyImage.__hash__()
		self.openImage = wx.Image('res/open_slot.png')
		self.bmpW,self.bmpH= self.getBitmapSize(self.Size) #initialize bitmapsizeparameter
		self.emptyBitMap = copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #leave our original copy!
		self.openBitMap = copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #leave our original copy!
		self.typeToImage = {} #associate types with images for rescaling purposes
		self.typeToBitmap = {} #associate types with bitmaps for drawing purposes
		###there is a better way to do this, likely it will involve rewritting this using the wrapper I use already, just throughout all...ffs.
		self.lastSize = self.GetClientSize()
		self.wrappedComponents = {} #map from component to wrappedComponent
		self.currentComponent = None

		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


	# Fired whenever a paint event occurs
	def OnPaint(self, evt):
		"""fired whenever a paint event occurs, i.e. Refresh() or Update"""
		#does not need to paint background, only what has changed...
		op = wx.COPY
		dc = wx.PaintDC(self) #grab device context
		self.PrepareDC(dc) #prepare
		if self.currentComponent != None: #if we have a component that is being put on the board by the user	
			self.currentComponent.drawSelf(dc,op,self.bmpW,self.bmpH) #tell it to paint itself.
	
	def OnLeftDown(self, evt):
		"""fired whenever left button is clicked"""
		posx,posy = evt.GetPosition()
		xLoc = posx//self.bmpW
		yLoc = posy//self.bmpH
		if self.currentComponent!= None: #we are moving something
			print (xLoc,yLoc)
			print id(self.currentComponent.breadboardComponent)
			print self.breadboard.putComponent(self.currentComponent.breadboardComponent,xLoc,yLoc)
			self.currentComponent = None

	# Left mouse button up.
	def OnLeftUp(self, evt):
		pass

	def OnSize(self,event):
		#event.Skip(
		self.Refresh()

	# The mouse is moving
	
	def OnMotion(self, evt):
		# Ignore mouse movement if we're not dragging.
		pos = self.ScreenToClient(wx.GetMousePosition())
		#print pos

		if self.buttonManager == None or self.buttonManager.currentButton == None:
			return
		else:
			if self.currentComponent == None:
				if self.buttonManager.currentName in self.typeToImage:
					self.loadTypeImage(self.buttonManager.currentName)
				self.currentComponent = BreadboardComponentWrapper(OpAmp('MINCH'),wx.Image('res/components/opamp_image.png').Rescale(4*self.bmpW,4*self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap())
				self.currentComponent.pos = pos
			else:
				self.currentComponent.pos = pos
			self.Refresh()
			self.Update()


	def getBitmapSize(self,size):
		return (size[0]//self.breadboard.numColumns,size[1]//self.breadboard.numRows)
	
	def OnEraseBackground(self, evt):
		dc = evt.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.PaintBackground(dc)
	
	def PaintBackground(self,dc):
		rescale = False
		if self.lastSize != self.GetClientSize():
			self.lastSize = self.GetClientSize()
			self.bmpW,self.bmpH= self.getBitmapSize(self.lastSize)
			self.emptyBitMap = copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #leave our original copy!
			self.openBitMap = copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #leave our original copy!			
			rescale = True

		for y in range(self.breadboard.numRows):	
			for x in range(self.breadboard.numColumns):
				isBlank = self.breadboard.getLocation(x,y).displayFlag != Location.OPENSLOT
				if isBlank: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					dc.DrawBitmap(self.emptyBitMap, x*self.bmpW, y*self.bmpH)
				else:
					dc.DrawBitmap(self.openBitMap, x*self.bmpW, y*self.bmpH) 
		self.PaintBreadboardComponents(dc,rescale)
				
	def PaintBreadboardComponents(self,dc,rescale):
		"""paint all components, pass in devic context and whether or not we have been scaled since last redraww"""
		for component in self.breadboard.componentList:
			if not component in self.wrappedComponents.keys():
				if isinstance(component, FixedBreadboardComponent):
					self.wrappedComponents[component] = FixedBreadboardComponentWrapper(self,component)
				else:
					self.wrappedComponents[component] = VariableBreadboardComponentWrapper(self,component)
			self.wrappedComponents[component].drawSelf(dc,rescale)
		if len(self.wrappedComponents.keys()) > len(self.breadboard.componentList):
			print "something was deleted, dolphin you need to fix this"

	def OnEraseBackground(self, evt):
		dc = evt.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.PaintBackground(dc)

	def loadTypeImage(self,typeName,instance=None):
		print "loading %s" %typeName
		temp =wx.Image('res/components/' + typeName.lower()+'_image.png')
		self.typeToImage[typeName] = copy.copy(temp)
		if instance != None: #we were passed an instance, and can create and size the bitmap
			self.typeToBitmap[typeName] = copy.copy(self.typeToImage[typeName]).Rescale(instance.width*self.bmpW,instance.height*self.bmpH).ConvertToBitmap()
		else:
			self.typeToBitmap[typeName] = None #stop keyerrors
			
	def getLoc(self,xy):
		return (xy[0]//self.bmpW,xy[1]//self.bmpH)
		
	def getXY(self,loc):
		return (loc[0]*self.bmpW,loc[1]*self.bmpH)
		
	def getCenteredXY(self,loc):	
		return ((loc[0]*self.bmpW) +(self.bmpW/2) ,(loc[1]*self.bmpH) + (self.bmpW/2)) #because we are drawing from top left, center is half of both down

class BreadboardComponentWrapper:
	"""Wraps an image, a bbc and a position for ease of use."""
	def __init__(self,breadboardComponent,bmp1,bmp2=None):
		self.bmp1 = bmp1
		self.bmp2 = bmp2
		self.pos = (0,0)
		self.breadboardComponent = breadboardComponent
	
	def drawSelf(self,dc,op,bmpW,bmpH):
		if self.bmp1.Ok():
			memDC = wx.MemoryDC()
			memDC.SelectObject(self.bmp1)
			dc.Blit(self.pos[0], self.pos[1]-(self.breadboardComponent.height*bmpH),self.bmp1.GetWidth(), self.bmp1.GetHeight(),memDC, 0, 0, op, True)
 
class VariableBreadboardComponentWrapper:
	"""this needed to happen"""
	def __init__(self,breadboardPanel,variableBreadboardComponent):
		self.bbp = breadboardPanel
		self.vbbc = variableBreadboardComponent
		self.typeName= type(self.vbbc).__name__
		#main image of this component's center
		if not self.typeName in self.bbp.typeToImage.keys():
			self.bbp.loadTypeImage(self.typeName)
		#image of the wire....
		if not BreadboardPanel.PLAINWIRE in self.bbp.typeToImage.keys():
			self.bbp.loadTypeImage(BreadboardPanel.PLAINWIRE)
		self.mainBMP = None #will be created on first draw
		self.wireBMP = None #will be created on first draw
		
	def drawSelf(self,dc,rescale,xyopt1=None,xyopt2=None):
		"""draw this vbbc. optionally, if xy1 and xy2 are non None, draw it between the two XY's,
		 instead of the locations, which may not be absolute"""
		if xyopt1 != None or xyopt2 != None:
			print "Cory get yo shit together"
		
		x1,y1 = self.bbp.getCenteredXY(self.vbbc.pinList[0].getLocationTuple())
		x2,y2 = self.bbp.getCenteredXY(self.vbbc.pinList[1].getLocationTuple())		
		dx,dy = (x2-x1,y2-y1)
		disp = self.vbbc.pinList[0].displacementTo(self.vbbc.pinList[1])
		theta = -3.14/2#this needs an answer....
		totalLength = math.sqrt(dx**2 + dy**2)	
		if rescale or self.mainBMP == None or self.wireBMP == None:
		#	self.mainBMP = copy.copy(self.bbp.typeToImage[self.typeName]).Rotate(theta).Rescale(self.bbp.bmpW*2,self.bmpH).ConvertToBitmap()
			tImage = copy.copy(self.bbp.typeToImage[BreadboardPanel.PLAINWIRE])
			tImage.Rescale(totalLength,tImage.GetHeight())
			self.wireBMP = tImage.Rotate(theta,(0,tImage.GetHeight()/2)).ConvertToBitmap()
#		if math.sqrt(disp[0]**2 + disp[1]**2) < 1:
			#just draw the damn centerpiece!
			
			#there is a sin/cos term here, we need to shift by some amount...		
		dc.DrawBitmap(self.wireBMP, x1, y1-(self.wireBMP.GetHeight()/2))
		dc.SetPen( wx.Pen( wx.Color(255,0,0), 5 ))
		dc.DrawLine(x1,y1,x2,y2)
		
class FixedBreadboardComponentWrapper:
	def __init__(self,breadboardPanel,fixedBreadboardComponent):
		self.bbp = breadboardPanel
		self.fbbc = fixedBreadboardComponent
		typeName= type(self.fbbc).__name__
		if not typeName in self.bbp.typeToImage.keys():
			self.bbp.loadTypeImage(typeName,instance=self.fbbc)

	def drawSelf(self,dc,rescale):
		if rescale or self.bbp.typeToBitmap[type(self.fbbc).__name__] == None:
			self.bbp.typeToBitmap[type(self.fbbc).__name__] = copy.copy(self.bbp.typeToImage[type(self.fbbc).__name__]).Rescale(self.bbp.bmpW*self.fbbc.width,self.bbp.bmpH*self.fbbc.height,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
		x,y = self.bbp.getXY(self.fbbc.pinList[0].getLocationTuple())
		y -= self.bbp.bmpH * (self.fbbc.height -1)
		dc.DrawBitmap(self.bbp.typeToBitmap[type(self.fbbc).__name__], x, y)


class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent, title=title)
		bb = Breadboard()		
		a = OpAmp('hello')
		c = Resistor(10)
		print bb.putComponent(c,3,3,3,7)
		print bb.putComponent(a,8,7)
		BreadboardPanel(self,bb)
		self.Fit()
		self.Show()

if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
