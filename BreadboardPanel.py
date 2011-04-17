#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *
from PIL import Image

class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard,*args, **kwargs):
 		wx.Panel.__init__(self, parent,*args,**kwargs)
 		self.parent = parent
		self.breadBoard = breadBoard
		self.gs = wx.GridSizer(self.breadBoard.numRows, self.breadBoard.numColumns, 0, 0) #gridsizer with numRows rows and numCols col, 1 px padding
		self.bitmapToXY = {} #.Rescale(20,20,wx.IMAGE_QUALITY_HIGH)
		self.emptyBitMap = wx.Image('res/blank_slot.png').ConvertToBitmap()
		self.openBitMap = wx.Image('res/open_slot.png').ConvertToBitmap()
		
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isFilled = breadBoard.getLocation(x,y).isFilled
				if isFilled: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					bmp =wx.StaticBitmap(self, -1, bitmap=self.emptyBitMap,size=(15,15),style = wx.NO_BORDER) #-1 = no id, no border overrides default 3d bevel
				else:
					bmp =wx.StaticBitmap(self, -1, bitmap=self.openBitMap,size=(15,15),style = wx.NO_BORDER)
				self.bitmapToXY[bmp] = (x,y) #map this staticbitmap to a tuple of  x,y, location
				bmp.Bind(wx.EVT_MOTION, self.onMotion,id=-1) #bind generic onMotion event,
				self.gs.Add(bmp,0) #add to the grid sizer, with no id
		
		print ('%d locations present') %len(self.bitmapToXY.values())
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.SetSizerAndFit(self.gs) #set this panel's sizer as the grid sizer
		self.Layout()
		#self.Sizer.Fit(parent)

	def onMotion(self,event):
		print self.GetSize()
		"""A generic onMotion event, TODO:look at hierachy, which event is invoked first?		"""
		x,y= self.bitmapToXY.get(event.GetEventObject())
		print event.GetEventObject().GetSize()
		print self.breadBoard.getLocation(x,y)
		#print "motion event:", event.m_x, event.m_y
	def OnSize(self,event):
		print 'onsize'
		newXSize= self.GetSize().x/self.breadBoard.numColumns
		newYSize= self.GetSize().y/self.breadBoard.numRows
		for key in self.bitmapToXY:
			key.SetSize((newXSize,newYSize))
			key.Refresh()
		self.Refresh(eraseBackground=True)
		self.Layout()

			
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


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
