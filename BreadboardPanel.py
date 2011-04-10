#!/usr/bin/python
# -*- coding: utf-8 -*-

# size.py

import wx
from Breadboard import *

class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard):
		wx.Panel.__init__(self, parent)
		self.breadBoard = breadBoard
		self.gs = wx.GridSizer(self.breadBoard.numRows, self.breadBoard.numColumns, 1, 1) #gridsizer with numRows rows and numCols col, 1 px padding
		self.bitmapToXY = {} #
		emptyBitMap = wx.Image('res/blank_slot.png').Scale(15,15,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
		openBitMap = wx.Image('res/open_slot.png').Scale(15,15,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isFilled = breadBoard.getLocation(x,y).isFilled
				if isFilled: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					bmp =wx.StaticBitmap(self, -1, bitmap=emptyBitMap,size=(15,15),style = wx.NO_BORDER) #-1 = no id, no border overrides default 3d bevel
				else:
					bmp =wx.StaticBitmap(self, -1, bitmap=openBitMap,size=(15,15),style = wx.NO_BORDER)
				self.bitmapToXY[bmp] = (x,y) #map this staticbitmap to a tuple of  x,y, location
				bmp.Bind(wx.EVT_MOTION, self.onMotion,id=-1) #bind generic onMotion event,
				self.gs.Add(bmp,0) #add to the grid sizer, with no id
		print ('%d locations present') %len(self.someDict.values())
		self.SetSizer(self.gs) #set this panel's sizer as the grid sizer
	def onMotion(self,event):
		
		x,y= self.someDict.get(event.GetEventObject())
		print self.breadBoard.getLocation(x,y)
		#print "motion event:", event.m_x, event.m_y

		
class Example(wx.Frame):
  
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(700, 300))
		BreadboardPanel(self,Breadboard())
		self.Show()


if __name__ == '__main__':
  
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
