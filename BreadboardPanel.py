#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *
import copy


class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard,buttonManager=None, *args, **kwargs):
 		wx.Panel.__init__(self, parent,size=(945,270),*args,**kwargs)
 		self.parent = parent
		self.breadBoard = breadBoard
		self.buttonManager = buttonManager

		self.emptyImage = wx.Image('res/blank_slot.png')
		print self.emptyImage.__hash__()
		self.openImage = wx.Image('res/open_slot.png')
		self.bmpW,self.bmpH= self.getBitmapSize(self.Size) #initialize bitmapsizeparameter
		self.emptyBitMap = copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #leave our original copy!
		self.openBitMap = copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #leave our original copy!
		self.typeToImage = {} #associate types with images for rescaling purposes
		self.typeToBitmap = {} #associate types with bitmaps for drawing purposes
		self.lastSize = self.GetClientSize()			
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
		op = wx.COPY
		dc = wx.PaintDC(self)
		self.PrepareDC(dc)
		if self.currentComponent != None:	
			if self.currentComponent.bmp1.Ok():
				memDC = wx.MemoryDC()
				memDC.SelectObject(self.currentComponent.bmp1)
				dc.Blit(self.currentComponent.pos[0], self.currentComponent.pos[1],self.currentComponent.bmp1.GetWidth(), self.currentComponent.bmp1.GetHeight(),memDC, 0, 0, op, True)

	# Left mouse button is down.
	def OnLeftDown(self, evt):
		posx,posy = evt.GetPosition()
		xLoc = posx//self.bmpW
		yLoc = posy//self.bmpH
		if self.currentComponent!= None:
			print (xLoc,yLoc)
			print id(self.currentComponent.breadboardComponent)
			print self.breadBoard.putComponent(self.currentComponent.breadboardComponent,xLoc,yLoc)
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
				self.currentComponent = BreadboardComponentWrapper(OpAmp('MINCH'),wx.Image('res/components/OpAmp_image.png').Rescale(4*self.bmpW,4*self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap())
				self.currentComponent.pos = pos
			else:
				self.currentComponent.pos = pos
			self.Refresh()
			self.Update()


	def getBitmapSize(self,size):
		return (size[0]//self.breadBoard.numColumns,size[1]//self.breadBoard.numRows)
	
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
			print self.emptyImage.__hash__()

		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isBlank = self.breadBoard.getLocation(x,y).displayFlag != Location.OPENSLOT
				if isBlank: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					dc.DrawBitmap(self.emptyBitMap, x*self.bmpW, y*self.bmpH)
				else:
					dc.DrawBitmap(self.openBitMap, x*self.bmpW, y*self.bmpH) 
		self.PaintBreadBoardComponents(dc,rescale)
				
	def PaintBreadBoardComponents(self,dc,rescale):
		for component in self.breadBoard.componentList:
			typeName= type(component).__name__
			if not typeName in self.typeToImage:
				self.loadTypeImage(typeName)
			if rescale:
				self.typeToBitmap[typeName] = copy.copy(self.typeToImage[typeName]).Rescale(self.bmpW*component.width,self.bmpH*component.height,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
			if isinstance(component, FixedBreadboardComponent):
				x,y = self.getXY(component.pinList[0].getLocationTuple())
				dc.DrawBitmap(self.typeToBitmap[typeName], x, y)
			else:
				print "this is a flexible component...Cory needs to get smaart"
				x1,y1 = self.getXY(component.pinList[0].getLocationTuple())
				x2,y2 = self.getXY(component.pinList[1].getLocationTuple())
				dc.DrawLine(x1,y1,x2,y2)

	def OnEraseBackground(self, evt):
		dc = evt.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.PaintBackground(dc)

	def loadTypeImage(self,typeName):
		temp =wx.Image('res/components/' + typeName+'_image.png')
		self.typeToImage[typeName] = copy.copy(temp)
		self.typeToBitmap[typeName] = copy.copy(temp.Rescale(self.bmpW*4,self.bmpH*4).ConvertToBitmap())

	def getLoc(self,xy):
		return (xy[0]//self.bmpW,xy[1]//self.bmpH)
		
	def getXY(self,loc):
		return (loc[0]*self.bmpW,loc[1]*self.bmpH)

class BreadboardComponentWrapper:
	"""Wraps an image, a bbc and a position for ease of use."""
	def __init__(self,breadboardComponent,bmp1,bmp2=None):
		self.bmp1 = bmp1
		self.bmp2 = bmp2
		self.pos = (0,0)
		self.breadboardComponent = breadboardComponent
	

class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent, title=title)
		
		bb = Breadboard()		
		a = OpAmp('hello')
		bb.putComponent(a,3,7)	
		BreadboardPanel(self,bb)
		self.Fit()
		self.Show()

if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
