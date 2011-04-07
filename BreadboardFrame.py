#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
import tkMessageBox

class BreadboardFrame(Frame):
	PIN_PIXEL_COUNT=8
	PADDING_PIXEL_COUNT = 1
	"""This is the GUI"""
	def __init__(self,breadBoard,master=None):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,master)
		self.master = master
		self.breadBoard = breadBoard
		"""Display the main window"
		with a little bit of padding"""
		self.grid(padx=10,pady=10)
		self.createWidgets()
		self.pack(fill=BOTH, expand=YES)
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.breadboardCanvas = BreadboardCanvas(self.breadBoard,master=self)
	def redraw(self):
		self.breadboardCanvas.canvas.delete(ALL)
		self.breadboardCanvas.drawBreadboard()

class BreadboardCanvas(object):
	def __init__(self,breadBoard,master=None,width=600,height=200):
		self.breadBoard = breadBoard
		self.canvas = Canvas(master=master,width=width,height=height)
		self.drawBreadboard()
		self.canvas.pack(fill=BOTH, expand=YES)
	
	def drawBreadboard(self):
		self.canvas.delete(ALL)
		for yNum in range(self.breadBoard.numRows):
			for xNum in range(self.breadBoard.numColumns):
				#print(yNum,xNum, breadBoard.getLocation(xNum,yNum).isFilled)
				startX = 1 + ((BreadboardFrame.PIN_PIXEL_COUNT+BreadboardFrame.PADDING_PIXEL_COUNT)*xNum)
				startY = 1 + ((BreadboardFrame.PIN_PIXEL_COUNT+BreadboardFrame.PADDING_PIXEL_COUNT)*yNum)
				color = 'green'
				if self.breadBoard.getLocation(xNum,yNum).isFilled:
					color = 'red'
				self.canvas.create_rectangle(startX,startY,startX+BreadboardFrame.PIN_PIXEL_COUNT,startY+BreadboardFrame.PIN_PIXEL_COUNT,fill=color)

if __name__ == "__main__":
	guiFrame = BreadboardFrame(Breadboard(),master=Tk())
	
	guiFrame.mainloop()

