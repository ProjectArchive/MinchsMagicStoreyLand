#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>

from Tkinter import *
from Breadboard import *
from BreadboardComponent import *
from BreadboardCanvas import *
from PartBrowserFrame import *
from PIL import Image,ImageTk 
from B2Spice import *


import tkMessageBox

class MainFrame(Frame):
	"""This is the GUI"""
	def __init__(self,breadBoard,**kw):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,**kw)
		self.master.title("Minch's Magic Storey Land!")
		self.breadBoard = breadBoard
		#self.master.rowconfigure( 0, weight = 1 )
		#self.master.columnconfigure( 0, weight = 1 )
		#self.grid( sticky = W+E+N+S )
		self.createWidgets()
		self.grid()

	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.createMenu()
		self.breadBoardCanvas = BreadboardCanvas(self.breadBoard,master=self)
		self.breadBoardCanvas.grid(row=1,column=1)
		self.partBrowserFrame = PartBrowserFrame(master=self)
		self.partBrowserFrame.grid(row=2,column =2)
		self.createSimulateButton()
		self.simulateButton.grid(row=1,column=3,sticky=N+E)

	def createMenu(self):
		self.menu = Menu(self)
		self.master.config(menu=self.menu)
		self.filemenu = Menu(self.menu)
		self.menu.add_cascade(label="File", menu=self.filemenu)
		self.filemenu.add_command(label="New", command=self.callback)
		self.filemenu.add_command(label="Open...", command=self.callback)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.callback)
		self.helpmenu = Menu(self.menu)
		self.menu.add_cascade(label="Help", menu=self.helpmenu)
		self.helpmenu.add_command(label="About...", command=self.callback)

	def createSimulateButton(self):
		photo = Image.open("res/simulate_image.png")
		photo=ImageTk.PhotoImage(photo)
		self.simulateButton = Button(self,image=photo,command=self.startSimulation)
		self.simulateButton.photo = photo

	def callback():
		print 'callback'
	
	def startSimulation(self):
		print 'Start Simulation'
		simInstance = B2Spice(self.breadBoard)
		res = simInstance.loadBb()
		print res

if __name__ == "__main__":
	guiFrame = MainFrame(Breadboard(),master=Tk(),width=900,height=500)	
	guiFrame.mainloop()
