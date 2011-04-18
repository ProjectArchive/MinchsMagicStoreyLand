#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *
from PIL import Image

class BreadboardPanel(wx.Panel):
	def __init__(self, parent,breadBoard,*args, **kwargs):
 		wx.Panel.__init__(self, parent,*args,**kwargs)
 		self.parent = parent
		self.breadBoard = breadBoard
		self.gs = wx.GridSizer(self.breadBoard.numRows, self.breadBoard.numColumns, 0, 0) #gridsizer with numRows rows and numCols col, 1 px padding
		self.bitmapToXY = {} #.Rescale(20,20,wx.IMAGE_QUALITY_HIGH)
		self.drawBreadboard()
		self.shapes = []
		self.dragImage = None
		self.dragShape = None
		self.hiliteShape = None

		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		self.SetSizerAndFit(self.gs) #set this panel's sizer as the grid sizer
		self.Layout()
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

	def OnLeaveWindow(self, evt):
		pass

	# Go through our list of shapes and draw them in whatever place they are.
	def DrawShapes(self, dc):
		for shape in self.shapes:
			if shape.shown:
				shape.Draw(dc)

	# This is actually a sophisticated 'hit test', but in this
	# case we're also determining which shape, if any, was 'hit'.
	def FindShape(self, pt):
		for shape in self.shapes:
			if shape.HitTest(pt):
				return shape
		return None

	# Fired whenever a paint event occurs
	def OnPaint(self, evt):
		print 'print invoked'
		dc = wx.PaintDC(self)
		self.PrepareDC(dc)
		self.DrawShapes(dc)

	# Left mouse button is down.
	def OnLeftDown(self, evt):
		# Did the mouse go down on one of our shapes?
		shape = self.FindShape(evt.GetPosition())
		# If a shape was 'hit', then set that as the shape we're going to
		# drag around. Get our start position. Dragging has not yet started.
		# That will happen once the mouse moves, OR the mouse is released.
		if shape:
			self.dragShape = shape
			self.dragStartPos = evt.GetPosition()

	# Left mouse button up.
	def OnLeftUp(self, evt):
		if not self.dragImage or not self.dragShape:
			self.dragImage = None
			self.dragShape = None
			return

		# Hide the image, end dragging, and nuke out the drag image.
		self.dragImage.Hide()
		self.dragImage.EndDrag()
		self.dragImage = None

		if self.hiliteShape:
			self.RefreshRect(self.hiliteShape.GetRect())
			self.hiliteShape = None
		
	def OnSize(self,event):
		print 'onsize'
		newXSize= self.GetSize().x/self.breadBoard.numColumns
		newYSize= self.GetSize().y/self.breadBoard.numRows
		if newXSize >15:
			self.openBitMap = self.emptyBitMap
		event.Skip()

	# The mouse is moving
	def OnMotion(self, evt):
		# Ignore mouse movement if we're not dragging.
		if not self.dragShape or not evt.Dragging() or not evt.LeftIsDown():
			return
		# if we have a shape, but haven't started dragging yet
		if self.dragShape and not self.dragImage:
			# only start the drag after having moved a couple pixels
			tolerance = 2
			pt = evt.GetPosition()
			dx = abs(pt.x - self.dragStartPos.x)
			dy = abs(pt.y - self.dragStartPos.y)
			if dx <= tolerance and dy <= tolerance:
				return
			self.dragShape.shown = False
			self.RefreshRect(self.dragShape.GetRect(), True)
			self.Update()
			if self.dragShape.text:
				self.dragImage = wx.DragString(self.dragShape.text,
											  wx.StockCursor(wx.CURSOR_HAND))
			else:
				self.dragImage = wx.DragImage(self.dragShape.bmp,
											 wx.StockCursor(wx.CURSOR_HAND))

			hotspot = self.dragStartPos - self.dragShape.pos
			self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)
			self.dragImage.Move(pt)
			self.dragImage.Show()
		# if we have shape and image then move it, posibly highlighting another shape.
		elif self.dragShape and self.dragImage:
			onShape = self.FindShape(evt.GetPosition())
			unhiliteOld = False
			hiliteNew = False
			# figure out what to hilite and what to unhilite
			if self.hiliteShape:
				if onShape is None or self.hiliteShape is not onShape:
					unhiliteOld = True
			if onShape and onShape is not self.hiliteShape and onShape.shown:
				hiliteNew = True
			# if needed, hide the drag image so we can update the window
			if unhiliteOld or hiliteNew:
				self.dragImage.Hide()
			if unhiliteOld:
				dc = wx.ClientDC(self)
				self.hiliteShape.Draw(dc)
				self.hiliteShape = None
			if hiliteNew:
				dc = wx.ClientDC(self)
				self.hiliteShape = onShape
				self.hiliteShape.Draw(dc, wx.INVERT)
			# now move it and show it again if needed
			self.dragImage.Move(evt.GetPosition())
			if unhiliteOld or hiliteNew:
				self.dragImage.Show()

	def drawBreadboard(self):
		##this needs to be updated... add dynamic dictionary to deal with redrawing
		self.emptyBitMap = wx.Image('res/blank_slot.png').ConvertToBitmap()
		self.openBitMap = wx.Image('res/open_slot.png').ConvertToBitmap()
		for y in range(self.breadBoard.numRows):	
			for x in range(self.breadBoard.numColumns):
				isFilled = self.breadBoard.getLocation(x,y).isFilled
				if isFilled: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					bmp =wx.StaticBitmap(self, -1, bitmap=self.emptyBitMap,size=(15,15),style = wx.NO_BORDER) #-1 = no id, no border overrides default 3d bevel
				else:
					bmp =wx.StaticBitmap(self, -1, bitmap=self.openBitMap,size=(15,15),style = wx.NO_BORDER)
				self.bitmapToXY[bmp] = (x,y) #map this staticbitmap to a tuple of  x,y, location
				bmp.Bind(wx.EVT_MOTION, self.onMotion,id=-1) #bind generic onMotion event,
				self.gs.Add(bmp,0) #add to the grid sizer, with no id





class BreadboardComponentWrapper:
    def __init__(self, bmp,BreadboardComponent):
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False


		
class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent, title=title)
		BreadboardPanel(self,Breadboard())
		self.Fit()
		self.Show()


class DragShape:
	def __init__(self, bmp):
		self.bmp = bmp
		self.pos = (0,0)
		self.shown = True
		self.text = None
		self.fullscreen = False

	def HitTest(self, pt):
		rect = self.GetRect()
		return rect.InsideXY(pt.x, pt.y)

	def GetRect(self):
		return wx.Rect(self.pos[0], self.pos[1],
					  self.bmp.GetWidth(), self.bmp.GetHeight())

	def Draw(self, dc, op = wx.COPY):
		if self.bmp.Ok():
			memDC = wx.MemoryDC()
			memDC.SelectObject(self.bmp)

			dc.Blit(self.pos[0], self.pos[1],
					self.bmp.GetWidth(), self.bmp.GetHeight(),
					memDC, 0, 0, op, True)

			return True
		else:
			return False


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
