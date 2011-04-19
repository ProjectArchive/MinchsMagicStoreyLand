#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *

class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard,buttonManager=None, *args, **kwargs):
 		wx.Panel.__init__(self, parent,*args,**kwargs)
 		self.parent = parent
		self.breadBoard = breadBoard
		self.buttonManager = buttonManager
		self.gs = wx.GridSizer(self.breadBoard.numRows, self.breadBoard.numColumns, 0, 0) #gridsizer with numRows rows and numCols col, 1 px padding
		self.bitmapToXY = {} #.Rescale(20,20,wx.IMAGE_QUALITY_HIGH)
		self.drawBreadboard()
		self.shapes = []
		self.dragImage = None
		self.dragShape = None
		self.hiliteShape = None

		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		self.currentMovableImage = None
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
		self.SetSizerAndFit(self.gs) #set this panel's sizer as the grid sizer
		self.Layout()
		print self.Size


	def OnLeaveWindow(self, evt):
		pass

	# Go through our list of shapes and draw them in whatever place they are.
	def DrawShapes(self, dc):
		for shape in self.shapes:
			if shape.shown:
				shape.Draw(dc)

	# This is actually a sophisticated 'hit test', but in this
	# case we're also determining which shape, if any, was 'hit'.
	def FindShape(self, pt):
		for shape in self.shapes:
			if shape.HitTest(pt):
				return shape
		return None

	# Fired whenever a paint event occurs
	def OnPaint(self, evt):
		print 'print invoked'
		dc = wx.PaintDC(self)
		self.PrepareDC(dc)
		self.DrawShapes(dc)

	# Left mouse button is down.
	def OnLeftDown(self, evt):
		print evt.GetEventObject().Size


	# Left mouse button up.
	def OnLeftUp(self, evt):
		print evt.GetEvent
		
	def OnSize(self,event):
		print 'onsize',self.Size
		event.Skip()

	# The mouse is moving
	
	def OnMotion(self, evt):
		# Ignore mouse movement if we're not dragging.
		pos = self.ScreenToClient(wx.GetMousePosition())
		#print pos
		if self.buttonManager.currentButton == None:
			return
		else:
			if self.currentMovableImage == None:
				self.tempBitmap = wx.Image('res/components/8pinopamp.png').ConvertToBitmap()
				self.currentMovableImage = wx.StaticBitmap(self,wx.ID_ANY,self.tempBitmap,pos=pos)
				self.currentMovableImage.initialPos = pos
				print pos
			else:
				self.currentMovableImage.Move(pos)
				print pos

	def drawBreadboard(self):
		##this needs to be updated... add dynamic dictionary to deal with redrawing
		self.emptyBitMap = wx.Image('res/blank_slot.png').ConvertToBitmap()
		self.openBitMap = wx.Image('res/open_slot2.png').ConvertToBitmap()
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isFilled = self.breadBoard.getLocation(x,y).isFilled
				if isFilled: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					bmp =wx.StaticBitmap(self, wx.ID_ANY, bitmap=self.emptyBitMap,size=(15,15),style = wx.NO_BORDER) #-1 = no id, no border overrides default 3d bevel
				else:
					bmp =wx.StaticBitmap(self, wx.ID_ANY, bitmap=self.openBitMap,size=(15,15),style = wx.NO_BORDER)
				self.bitmapToXY[bmp] = (x,y) #map this staticbitmap to a tuple of  x,y, location
				bmp.Bind(wx.EVT_MOTION, self.OnMotion,id=wx.ID_ANY) #bind generic onMotion event,
				bmp.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
				self.gs.Add(bmp,0) #add to the grid sizer, with no id


class BreadboardComponentWrapper:
    def __init__(self, bmp,BreadboardComponent):
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.fullscreen = False

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

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False


		
class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent, title=title)
		BreadboardPanel(self,Breadboard())
		self.Fit()
		self.Show()


class DragShape:
	def __init__(self, bmp):
		self.bmp = bmp
		self.pos = (0,0)
		self.shown = True
		self.text = None
		self.fullscreen = False

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

			dc.Blit(self.pos[0], self.pos[1],
					self.bmp.GetWidth(), self.bmp.GetHeight(),
					memDC, 0, 0, op, True)

			return True
		else:
			return False


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
