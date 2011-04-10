#!/usr/bin/python
# -*- coding: utf-8 -*-

# size.py

import wx
from Breadboard import *

class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard):
		wx.Panel.__init__(self, parent)
		self.breadBoard = breadBoard
		vbox = wx.BoxSizer(wx.VERTICAL)
		gs = wx.GridSizer(self.breadBoard.numRows, self.breadBoard.numColumns, 1, 1)
		self.someDict = {}
		emptyBitMap = wx.Image('res/blank_slot.png').Scale(15,15,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
		openBitMap = wx.Image('res/open_slot.png').Scale(15,15,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isFilled = breadBoard.getLocation(x,y).isFilled
				print isFilled
				if isFilled:
					bmp =wx.StaticBitmap(self, -1, bitmap=emptyBitMap,size=(15,15),style = wx.NO_BORDER)
				else:
					bmp =wx.StaticBitmap(self, -1, bitmap=openBitMap,size=(15,15),style = wx.NO_BORDER)
				self.someDict[bmp] = (x,y)
				bmp.Bind(wx.EVT_MOTION, self.onMotion,id=-1)
				gs.Add(bmp,0)
		print len(self.someDict.values())
		vbox.Add(gs,flag=wx.EXPAND)
		self.SetSizer(vbox)
	def onMotion(self,event):
		print self.someDict.get(event.GetEventObject())
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
