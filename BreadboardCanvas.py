#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from copy import *
import tkMessageBox
class BreadboardCanvas(Canvas):

	def __init__(self,breadBoard,**kw):
		Canvas.__init__(self,height=170,width=580,**kw)
		self.lastLoc = None
		self.PXPERx = 8
		self.PXPERy = 8
		self.breadBoard = breadBoard
		self.idToLoc = dict()
		self.drawBreadboard()
		self.bind("<Button-1>", self.click)
		
	def drawBreadboard(self):
		for yNum in range(self.breadBoard.numRows):
			for xNum in range(self.breadBoard.numColumns):
				#print(yNum,xNum, breadBoard.getLocation(xNum,yNum).isFilled)
				startX = 1 + ((self.PXPERx+1)*xNum)
				startY = 1 + ((self.PXPERy+1)*yNum)
				color = 'green'
				tLoc =self.breadBoard.getLocation(xNum,yNum) 
				if tLoc.isFilled:
					color = 'red'
				tempItem = self.create_rectangle(startX,startY,startX+self.PXPERx,startY+self.PXPERy,fill=color)
				self.idToLoc[tempItem] = tLoc
	def reDraw(self):
		self.delete(ALL)
		self.drawBreadboard()

	def click(self,event):
		if self.find_withtag(CURRENT):
			self.itemconfig(CURRENT, fill="blue") #illuminate target
			print 'lastloc:',self.lastLoc
			loc = self.idToLoc.get(self.find_withtag(CURRENT)[0],None)
			if self.master.partBrowserFrame.CURRENT != "":
				print self.master.partBrowserFrame.CURRENT,loc
				if self.lastLoc != None:
					if self.master.partBrowserFrame.CURRENT == "RESISTOR":
						print 'placing resistor'
						tRes = Resistor(50)
						success =self.breadBoard.putComponent(tRes,self.lastLoc.xLoc,self.lastLoc.yLoc,loc.xLoc,loc.yLoc)
						print 'placed',tRes, success
					elif self.master.partBrowserFrame.CURRENT == "CAPACITOR":
						print 'placing capacitor'
						tCap = Capacitor(50)
						success =self.breadBoard.putComponent(tCap,self.lastLoc.xLoc,self.lastLoc.yLoc,loc.xLoc,loc.yLoc)
						print 'placed',tCap, success
					elif self.master.partBrowserFrame.CURRENT == "WIRE":
						print 'placing wire'
						tWire = Wire()
						success =self.breadBoard.putComponent(tWire,self.lastLoc.xLoc,self.lastLoc.yLoc,loc.xLoc,loc.yLoc)
						print 'placed',tWire, success
					self.lastLoc = None #we have placed something, reset lastLoc									
					self.reDraw() #redraw self
				else:
					self.lastLoc = loc
			else:
				print loc
				self.lastLoc = None
				self.itemconfig(CURRENT, fill="blue")
			self.update_idletasks()
			self.after(200)
			if loc.isFilled:
				self.itemconfig(CURRENT, fill="red")
			else:
				self.itemconfig(CURRENT, fill="green")
				
"""
This modle <Item> is part of Swampy, a suite of programs available from
allendowney.com/swampy.
Copyright 2005 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""
class Item(object):
    """Represents a canvas item.

    When you create a canvas item, Tkinter returns an integer 'tag'
    that identifies the new item.  To perform an operation on the
    item, you invoke a method on the canvas and pass the tag as
    a parameter.

    The Item class makes this interface more object-oriented:
    each Item object contains a canvas and a tag.  When you
    invoke methods on the Item, it invokes methods on its canvas.
    """
    def __init__(self, canvas, tag):
        self.canvas = canvas
        self.tag = tag

    def __str__(self):
        return str(self.tag)
        
    # the following are wrappers for canvas methods

    def delete(self):
        """Deletes this item from the canvas."""
        self.canvas.delete(self.tag)

    def cget(self, *args):
        """Looks up the value of the given option for this item."""
        return self.canvas.itemcget(self.tag, *args)
        
    def config(self, **options):
        """Reconfigures this item with the given options."""
        self.canvas.itemconfig(self.tag, **options)

    def coords(self, *args):
        """Gets or sets the canvas coordinates for this item."""
        return self.canvas.canvas_itemcoords(self.tag, *args)

    def bbox(self):
        """Get the approximate bounding box for this item.

        Returns:
            BBox object in canvas coordinates.
        """
        return self.canvas.bbox(self.tag)

    def bind(self, event, *args):
        """Applies a binding to this item.

        args can be (event, callback) or (event, callback, '+')

        For the event specifier, you can use Tkinter format,
        as in <Button-1>, or you can leave out the angle brackets.
        """
        if event[0] != '<':
            event = '<' + event + '>'
        event = self.canvas.translate_event(event)
        self.canvas.tag_bind(self.tag, event, *args)

    def unbind(self, *args):
        """Removes bindings from this items."""
        self.canvas.tag_unbind(self.tag, *args)

    def type(self):
        """Returns a string indicating the type of this item."""
        return self.canvas.type(self.tag)

    def lift(self):
        """Raises this item to the top of the pile."""
        return self.canvas.lift(self.tag)

    def lower(self):
        """Lowers this item to the bottom of the pile."""
        return self.canvas.lower(self.tag)

    def move(self, dx, dy):
        """Moves this item by (dx, dy) in canvas coordinates."""
        self.canvas.move(self.tag, dx, dy)

    def move_coord(self, i, dx, dy):
        """Moves the ith coordinate by (dx, dy) in canvas coordinates."""
        coords = self.coords()
        coords[i][0] += dx
        coords[i][1] += dy
        self.coords(coords)

    def replace_coord(self, i, coord):
        """Replaces the ith coordinate with the given coordinate."""
        coords = self.coords()
        coords[i] = coord
        self.coords(coords)

    def scale(self, scale, offset):
        """Shifts and scales the coordinates of this item.

        Shifts by -(offset) and multiplies by (scale)
        """
        xscale, yscale = scale
        xoffset, yoffset = offset
        self.canvas.scale(self.tag, xscale, yscale, xoffset, yoffset)

if __name__ == "__main__":
	guiFrame = BreadboardCanvas(Breadboard(),master=Tk())
	guiFrame.pack()
	guiFrame.mainloop()

