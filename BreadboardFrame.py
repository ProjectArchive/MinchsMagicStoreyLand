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
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.breadboardCanvas = BreadboardCanvas(self.breadBoard,master=self)
	def redraw(self):
		self.breadboardCanvas.canvas.delete(ALL)
		self.breadboardCanvas.drawBreadboard()

class BreadboardCanvas(object):
	def __init__(self,breadBoard,master=None,width=480,height=200):
		self.breadBoard = breadBoard
		self.canvas = Canvas(master=master,width=width,height=height)
		self.drawBreadboard()
		#self.canvas.pack()
		self.canvas.pack(padx=self.padX,pady=self.padY)
	
	def drawBreadboard(self):
		self.PXPERx=(int(self.canvas.cget('width'))-(self.breadBoard.numColumns))/self.breadBoard.numColumns
		self.PXPERy=(int(self.canvas.cget('height'))-(self.breadBoard.numRows))/self.breadBoard.numRows
		self.padX = int(self.canvas.cget('width')) -(self.breadBoard.numColumns*(self.PXPERx+1))
		self.padY = int(self.canvas.cget('height')) -(self.breadBoard.numRows*(self.PXPERy+1))

		self.canvas.delete(ALL)
		for yNum in range(self.breadBoard.numRows):
			for xNum in range(self.breadBoard.numColumns):
				#print(yNum,xNum, breadBoard.getLocation(xNum,yNum).isFilled)
				startX = 1 + ((self.PXPERx+1)*xNum)
				startY = 1 + ((self.PXPERy+1)*yNum)
				color = 'green'
				if self.breadBoard.getLocation(xNum,yNum).isFilled:
					color = 'red'
				self.canvas.create_rectangle(startX,startY,startX+self.PXPERx,startY+self.PXPERy,fill=color)
		
		
if __name__ == "__main__":
	guiFrame = BreadboardFrame(Breadboard(),master=Tk())
	
	guiFrame.mainloop()

