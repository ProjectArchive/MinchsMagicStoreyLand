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
		self.openImage = wx.Image('res/open_slot.png')
		self.bmpW,self.bmpH= self.getBitmapSize(self.Size) #initialize bitmapsizeparameter
		self.emptyBitMap = copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH).ConvertToBitmap() #leave our original copy!
		self.openBitMap = copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH).ConvertToBitmap() #leave our original copy!
		self.typeToImage = {} #associate types with images for rescaling purposes
		self.typeToBitmap = {} #associate types with bitmaps for drawing purposes
		self.currentComponent = None
		self.lastSize = self.GetClientSize()


		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


	# This is actually a sophisticated 'hit test', but in this
	# case we're also determining which shape, if any, was 'hit'.
	def FindShape(self, pt):
		for shape in self.shapes:
			if shape.HitTest(pt):
				return shape
		return None

	# Fired whenever a paint event occurs
	def OnPaint(self, evt):
		op = wx.COPY
		print 'paint invoked'
		dc = wx.PaintDC(self)
		self.PrepareDC(dc)
		if self.currentComponent != None:
			self.currentComponent.Draw(dc)

			
	# Left mouse button is down.
	def OnLeftDown(self, evt):
		if self.buttonManager == None or self.buttonManager.currentButton == None:
			return
		posx,posy = evt.GetPosition()
		xLoc = posx//self.bmpW
		yLoc = posy//self.bmpH
		print (xLoc,yLoc)
		if self.currentComponent != None:
			success =self.breadBoard.putComponent(self.currentComponent.breadBoardComponent,xLoc,yLoc)
			if success:
				del self.currentComponent
				self.currentComponent = None
			print success
	# Left mouse button up.
	def OnLeftUp(self, evt):
		pass
		
		
	def OnSize(self,event):
		#event.Skip()
		self.Refresh()

	# The mouse is moving
	
	def OnMotion(self, evt):
		# Ignore mouse movement if we're not dragging.
		pos = self.ScreenToClient(wx.GetMousePosition())
		#print pos

		if self.buttonManager == None or self.buttonManager.currentButton == None:
			if self.currentComponent != None:
				self.currentComponent = None # make sure it is nullified
			return
		else:
			if self.currentComponent == None:
				if not self.buttonManager.currentName in self.typeToBitmap:
					self.loadTypeImage(self.buttonManager.currentName)
				self.currentComponent = BreadboardComponentWrapper(self.typeToBitmap[self.buttonManager.currentName],OpAmp('MINCH'))
			
			self.currentComponent.pos = pos
			self.currentComponent.shown = False
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
			rescale = True
			self.bmpW,self.bmpH= self.getBitmapSize(self.Size)
			self.emptyBitMap = copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH).ConvertToBitmap() #leave our original copy!
			self.openBitMap = copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH).ConvertToBitmap() #leave our original copy!
			self.lastSize = self.GetClientSize()
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isBlank = self.breadBoard.getLocation(x,y).displayFlag != Location.OPENSLOT
				if isBlank: pass #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					#dc.DrawBitmap(self.emptyBitMap, x*self.bmpW, y*self.bmpH)
				else: pass
					#dc.DrawBitmap(self.openBitMap, x*self.bmpW, y*self.bmpH) 
		self.PaintBreadBoardComponents(dc,rescale)
				
	def PaintBreadBoardComponents(self,dc,rescale):

		for component in self.breadBoard.componentList:
			typeName= type(component).__name__
			if not typeName in self.typeToImage:
				self.loadTypeImage(typeName)
			if rescale:
				self.typeToBitmap[typeName] = copy.copy(self.typeToImage[typeName]).Rescale(component.width*self.bmpW,component.height*self.bmpH).ConvertToBitmap() #wow, long line...
			x,y = component.pinList[0].getLocationTuple()
			x*=self.bmpW
			y*=self.bmpH
			dc.DrawBitmap(self.typeToBitmap[typeName], x, y)
			

	def OnEraseBackground(self, evt):
		dc = evt.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.PaintBackground(dc)

	def loadTypeImage(self,typeName):
		##TODO:fix for non fixed and not opamp
		temp =wx.Image('res/components/' + typeName+'_image.png')
		self.typeToImage[typeName] = copy.copy(temp)
		self.typeToBitmap[typeName] = copy.copy(temp.Rescale(self.bmpW*4,self.bmpH*4).ConvertToBitmap())

class BreadboardComponentWrapper:
    def __init__(self, bmp,breadboardComponent):
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.fullscreen = False
        self.breadBoardComponent = breadboardComponent

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)
            dc.Blit(self.pos[0], self.pos[1],self.bmp.GetWidth(), self.bmp.GetHeight(),memDC, 0, 0, op, True)

            return True
        else:
            return False


		
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
