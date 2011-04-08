#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from BreadboardComponent import *
from BreadboardCanvas import *
from PartBrowserFrame import *
from PIL import Image,ImageTk
import B2SPice

import tkMessageBox

class MainFrame(Frame):
	"""This is the GUI"""
	def __init__(self,breadBoard,master=None):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,master)
		self.master = master
		self.master.title("Minch's Magic Storey Land!")
		self.breadBoard = breadBoard
		self.grid(padx=10,pady=10)
		self.createWidgets()		
	def placeAnOpAmp(self):
		self.breadBoard.putComponent(Resistor(100),1,1,2,2)
		print 'placed an op amp'
		self.breadBoardFrame.redraw()
		
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.breadBoardCanvas = BreadboardCanvas(self,self.breadBoard)
		self.breadBoardCanvas.grid(row=0,column=1)
		self.partBrowserFrame = PartBrowserFrame(master=self)
		self.partBrowserFrame.grid(row=1,column =0)
		self.createMenu()
		self.createSimulateButton()
		self.simulateButton.grid(row=1,column=2)
	
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
		
if __name__ == "__main__":
	guiFrame = MainFrame(Breadboard(),Tk())	
	guiFrame.mainloop()
