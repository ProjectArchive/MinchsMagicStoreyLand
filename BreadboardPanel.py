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
	def __init__(self, parent,breadBoard):
		wx.Panel.__init__(self, parent)
		self.breadBoard = breadBoard
		self.gs = wx.GridSizer(self.breadBoard.numRows, self.breadBoard.numColumns, 0, 0) #gridsizer with numRows rows and numCols col, 1 px padding
		self.bitmapToXY = {} #.Rescale(20,20,wx.IMAGE_QUALITY_HIGH)
		self.emptyBitMap = wx.Image('res/blank_slot.png').ConvertToBitmap()
		self.openBitMap = wx.Image('res/open_slot.png').ConvertToBitmap()
		
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isFilled = breadBoard.getLocation(x,y).isFilled
				if isFilled: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					bmp =wx.StaticBitmap(self, -1, bitmap=self.emptyBitMap,size=(50,50),style = wx.NO_BORDER) #-1 = no id, no border overrides default 3d bevel
				else:
					bmp =wx.StaticBitmap(self, -1, bitmap=self.openBitMap,size=(50,50),style = wx.NO_BORDER)
				self.bitmapToXY[bmp] = (x,y) #map this staticbitmap to a tuple of  x,y, location
				bmp.Bind(wx.EVT_MOTION, self.onMotion,id=-1) #bind generic onMotion event,
				self.gs.Add(bmp,0) #add to the grid sizer, with no id
		
		print ('%d locations present') %len(self.bitmapToXY.values())
		self.SetSizer(self.gs) #set this panel's sizer as the grid sizer

	def onMotion(self,event):
		"""A generic onMotion event, TODO:look at hierachy, which event is invoked first?		"""
		x,y= self.bitmapToXY.get(event.GetEventObject())
		print event.GetEventObject().GetSize()
		print self.breadBoard.getLocation(x,y)
		#print "motion event:", event.m_x, event.m_y

		
class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(1200, 700))
		BreadboardPanel(self,Breadboard())
		self.Show()


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
