#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from PIL import Image,ImageTk
import tkMessageBox

class PartBrowserFrame(Frame):
	"""This is the GUI"""
	def __init__(self,**kw):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,**kw)
		"""Display the main window"
		with a little bit of padding"""
		self.createWidgets()
		self.grid()
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		###make resistor button
		photo = Image.open("res/resistor_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 50), Image.ANTIALIAS))
		self.resistorButton = Button(image=photo,command=self.createResistorEvent)
		self.resistorButton.image = photo
		self.resistorButton.grid(row=0,column=1,padx=2,pady=2)
		###make capacitor button
		photo = Image.open("res/capacitor_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 50), Image.ANTIALIAS))
		self.capacitorButton = Button(image=photo,command=self.createCapacitorEvent)
		self.capacitorButton.image = photo
		self.capacitorButton.grid(row=0,column=2,padx=2,pady=2)
		###make wire button
		photo = Image.open("res/wire_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 50), Image.ANTIALIAS))
		self.wireButton = Button(image=photo,command=self.createWireEvent)
		self.wireButton.image = photo
		self.wireButton.grid(row=0,column=3,padx=2,pady=2)

	def createResistorEvent(self):
		isRaised = self.resistorButton.cget('relief') == "raised" 
		if isRaised:
			self.resistorButton.config(relief=SUNKEN)
		else:
			self.resistorButton.config(relief=RAISED)
		print 'create resistor event invoked'
		
	def createWireEvent(self):
		isRaised = self.resistorButton.cget('relief') == "raised" 
		if isRaised:
			self.resistorButton.config(relief=SUNKEN)
		else:
			self.resistorButton.config(relief=RAISED)
		print 'create resistor event invoked'
		
	def createCapacitorEvent(self):
		print 'create resistor event invoked'
		
if __name__ == "__main__":
	root = Tk()
	guiFrame = PartBrowserFrame(master=root)
	root.mainloop()

