#!/usr/bin/python
# -*- coding: utf-8 -*-

# size.py

import wx
import Breadboard

class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard):
		wx.Panel.__init__(self, parent)
		self.box = wx.BoxSizer(wx.VERTICAL)
		self.createBackgroundButtons()
		
	def createBackgroundButtons(self):
		self.box.Add(wx.Button(self, -1, 'Close'))
		self.box.Add(wx.Button(self, -1, 'Random Move'))
		self.box.Add(wx.Button(self, -1, 'Chmmm'))
		
class Example(wx.Frame):
  
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(400, 200))
		BreadboardPanel(self,None)
		self.Show()


if __name__ == '__main__':
  
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
