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
		self.breadboardCanvas = BreadboardCanvas(master=self,breadBoard=self.breadBoard,width=400,height=200)
		self.breadboardCanvas.drawBreadboard()
		self.breadboardCanvas.pack()

class BreadboardCanvas(Canvas):
	
	def __init__(self, master=None,breadBoard=None, **kw):
		Canvas.__init__(self,master,**kw)
		self.breadBoard = breadBoard
	
	def drawBreadboard(self):
		self.PXPERx=(int(self.cget('width'))-(self.breadBoard.numColumns))/self.breadBoard.numColumns
		self.PXPERy=(int(self.cget('height'))-(self.breadBoard.numRows))/self.breadBoard.numRows
		self.padX = int(self.cget('width')) -(self.breadBoard.numColumns*(self.PXPERx+1))
		self.padY = int(self.cget('height')) -(self.breadBoard.numRows*(self.PXPERy+1))
		self.delete(ALL)
		for yNum in range(self.breadBoard.numRows):
			for xNum in range(self.breadBoard.numColumns):
				#print(yNum,xNum, breadBoard.getLocation(xNum,yNum).isFilled)
				startX = 1 + ((self.PXPERx+1)*xNum)
				startY = 1 + ((self.PXPERy+1)*yNum)
				color = 'green'
				if self.breadBoard.getLocation(xNum,yNum).isFilled:
					color = 'red'
				self.create_rectangle(startX,startY,startX+self.PXPERx,startY+self.PXPERy,fill=color)
		
		
if __name__ == "__main__":
	guiFrame = BreadboardFrame(Breadboard(),master=Tk())
	
	guiFrame.mainloop()

