#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *
import math
import copy
import Image		# Pil package for rotation+filtering all-in-one.
import ImgConv	

class BreadboardPanel(wx.Panel):
	PLAINWIRE = "plainwire"
	def __init__(self, parent,breadboard,buttonManager=None, *args, **kwargs):
		kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
 		wx.Panel.__init__(self, parent,size=(945,270),*args,**kwargs)
 		self.parent = parent
		self.breadboard = breadboard
		self.buttonManager = buttonManager

		self.emptyImage = wx.Image('res/blank_slot.png',wx.BITMAP_TYPE_PNG)
		self.openImage = wx.Image('res/openslot_2.png',wx.BITMAP_TYPE_PNG)
		self.bmpW,self.bmpH= self.getBitmapSize(self.Size) #initialize bitmapsizeparameter
		self.emptyBitMap = wx.BitmapFromImage(copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH)) #leave our original copy!
		self.openBitMap = wx.BitmapFromImage(copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH)) #leave our original copy!
		self.typeToImage = {} #associate types with images for rescaling purposes
		self.typeToBitmap = {} #associate types with bitmaps for drawing purposes
		###there is a better way to do this, likely it will involve rewritting this using the wrapper I use already, just throughout all...ffs.
		self.lastSize = self.GetClientSize()
		self.wrappedComponents = {} #map from component to wrappedComponent
		self.currentComponent = None

		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
		
		
	def OnLeaveWindow(self,evt):
		self.currentComponent = None
		self.Refresh()
		self.Update()	

	# Fired whenever a paint event occurs
	def OnPaint(self, evt):
		"""fired whenever a paint event occurs, i.e. Refresh() or Update"""
		#does not need to paint background, only what has changed...
		op = wx.COPY
		dc = wx.PaintDC(self) #grab device context
		self.PrepareDC(dc) #prepare
		if self.currentComponent != None: #if we have a component that is being put on the board by the user	
			self.currentComponent.drawSelf(dc,op,self.bmpW,self.bmpH) #tell it to paint itself.
	
	
	
	def OnLeftDown(self, evt):
		"""fired whenever left button is clicked"""
		posx,posy = evt.GetPosition()
		xLoc = posx//self.bmpW
		yLoc = posy//self.bmpH
		if self.currentComponent!= None: #we are moving something
			print (xLoc,yLoc)
			if isinstance(self.currentComponent.breadboardComponent,FixedBreadboardComponent):
				if self.breadboard.putComponent(self.currentComponent.breadboardComponent,xLoc,yLoc):
					print "placed", self.currentComponent.breadboardComponent,xLoc,yLoc
				self.currentComponent = None
			else:
				if self.currentComponent.anchorPos == None:
					self.currentComponent.anchorPos = (xLoc,yLoc) #assign the first anchor
				else:
					if self.breadboard.putComponent(self.currentComponent.breadboardComponent,self.currentComponent.anchorPos[0],self.currentComponent.anchorPos[1],xLoc,yLoc):
						self.currentComponent = None
				
	# Left mouse button up.
	def OnLeftUp(self, evt):
		pass

	def OnSize(self,event):
		"""when resized... Just refresh, the actual computation of sizes occurs there, that should probably change..."""
		self.Refresh()

	# The mouse is moving
	
	def OnMotion(self, evt):
		"""Invoked when this panel receives an OnMotion event from the wx.App"""
		pos = self.ScreenToClient(wx.GetMousePosition())
		pos = (pos[0] -3,pos[1] +3)
		#print pos

		if self.buttonManager == None or self.buttonManager.currentButton == None:
			return
		else:
			if self.currentComponent == None:
				self.currentComponent = BreadboardComponentWrapper(self,self.getDefaultInstance(self.buttonManager.currentName),wx.Image('res/components/opamp_image.png').Rescale(4*self.bmpW,4*self.bmpH,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap())
				self.currentComponent.pos = pos
			else:
				self.currentComponent.pos = pos
			self.Refresh()
			self.Update()


	def getBitmapSize(self,size):
		"""Simple helper to get the current bitmap size for a single location"""
		return (size[0]//self.breadboard.numColumns,size[1]//self.breadboard.numRows)
	
	def OnEraseBackground(self, evt):
		"""erase background is called during certain paint events and when the canvas is damaged"""
		dc = evt.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.PaintBackground(dc)
	
	def PaintBackground(self,dc):
		rescale = False
		if self.lastSize != self.GetClientSize():
			self.lastSize = self.GetClientSize()
			self.bmpW,self.bmpH= self.getBitmapSize(self.lastSize)
			self.emptyBitMap = wx.BitmapFromImage(copy.copy(self.emptyImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH)) #leave our original copy!
			self.openBitMap = wx.BitmapFromImage(copy.copy(self.openImage).Rescale(self.bmpW,self.bmpH,wx.IMAGE_QUALITY_HIGH)) #leave our original copy!			
			rescale = True

		for y in range(self.breadboard.numRows):	
			for x in range(self.breadboard.numColumns):
				isBlank = self.breadboard.getLocation(x,y).displayFlag != Location.OPENSLOT
				if isBlank: #different images. Should add support for flags, i.e. red, blue striples and always filled, etc.
					dc.DrawBitmap(self.emptyBitMap, x*self.bmpW, y*self.bmpH)
				else:
					dc.DrawBitmap(self.openBitMap, x*self.bmpW, y*self.bmpH) 
		self.PaintBreadboardComponents(dc,rescale)
				
	def PaintBreadboardComponents(self,dc,rescale):
		"""paint all components, pass in devic context and whether or not we have been scaled since last redraww"""
		for component in self.breadboard.componentList:
			if not component in self.wrappedComponents.keys():
				if isinstance(component, FixedBreadboardComponent):
					self.wrappedComponents[component] = FixedBreadboardComponentWrapper(self,component)
				else:
					self.wrappedComponents[component] = VariableBreadboardComponentWrapper(self,component)
			self.wrappedComponents[component].drawSelf(dc,rescale)
		if len(self.wrappedComponents.keys()) > len(self.breadboard.componentList):
			print "something was deleted, dolphin you need to fix this"

	def OnEraseBackground(self, evt):
		dc = evt.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.PaintBackground(dc)

	def loadTypeImage(self,typeName,instance=None):
		print "loading %s" %typeName
		temp =wx.Image('res/components/' + typeName.lower()+'_image.png',wx.BITMAP_TYPE_PNG)
		if not temp.HasAlpha():
			temp.InitAlpha()
		self.typeToImage[typeName] = copy.copy(temp)
		if instance != None: #we were passed an instance, and can create and size the bitmap
			self.typeToBitmap[typeName] = wx.BitmapFromImage(copy.copy(self.typeToImage[typeName]).Rescale(instance.width*self.bmpW,instance.height*self.bmpH))
			self.typeToBitmap[typeName].SaveFile(typeName+".bmp", wx.BITMAP_TYPE_BMP)
		else:
			self.typeToBitmap[typeName] = None #stop keyerrors
			
	def getLoc(self,xy):
		return (xy[0]//self.bmpW,xy[1]//self.bmpH)
		
	def getXY(self,loc):
		return (loc[0]*self.bmpW,loc[1]*self.bmpH)
		
	def getCenteredXY(self,loc):	
		return ((loc[0]*self.bmpW) +(float(self.bmpW)/2) ,(loc[1]*self.bmpH) + (float(self.bmpW)/2)) #because we are drawing from top left, center is half of both down

	def getDefaultInstance(self,typeName):
		typeName = typeName.lower()
		if typeName.find('resistor') != -1:
			return Resistor(50)
		elif typeName.find('capacitor') != -1:
			return Capacitor(50)
		elif typeName.find('wire') != -1:
			return Wire()
		elif typeName.find('opamp') != -1:
			return OpAmp('OPA551')
		else:
			return None
	def killCurrent(self):
		self.wrappedComponents = {}


class BreadboardComponentWrapper:
	"""Wraps an image, a bbc and a position for ease of drawing while moving..."""
	def __init__(self,bbp,breadboardComponent,bmp1,bmp2=None):
		self.bbp = bbp
		self.bmp1 = bmp1
		self.bmp2 = bmp2
		self.pos = (0,0)
		self.anchorPos = None
		self.breadboardComponent = breadboardComponent
		self.typeName = type(self.breadboardComponent).__name__
	
	def drawSelf(self,dc,op,bmpW,bmpH):
		if isinstance(self.breadboardComponent,FixedBreadboardComponent):			
			if self.bmp1.Ok():
				memDC = wx.MemoryDC()
				memDC.SelectObject(self.bmp1)
				dc.Blit(self.pos[0], self.pos[1]-(self.breadboardComponent.height*bmpH),self.bmp1.GetWidth(), self.bmp1.GetHeight(),memDC, 0, 0, op, True)
		else:
			if self.anchorPos == None:
				return
			x1,y1 = self.bbp.getCenteredXY(self.anchorPos)
			x2,y2 = self.pos
			dx,dy = (x2-x1,y2-y1)
			totalLength = math.sqrt(dx**2 +dy**2)
			slopeX = dx/totalLength
			slopeY = dy/totalLength #slope of x with respect to length	

			dc.SetPen( wx.Pen( wx.Color(128,128,128),3))	
			dc.DrawLine(x1,y1,x2,y2)
			
			if self.typeName.lower().find('wire') != -1:
				dc.SetPen(wx.Pen(wx.Color(255,0,0),5))
				startX=x1 + (0.1*totalLength*slopeX)
				startY =y1 + (0.1*totalLength*slopeY)
				endX = startX+(0.8*totalLength*slopeX)
				endY = startY+(0.8*totalLength*slopeY)	
				dc.DrawLine(startX,startY,endX,endY)
			elif self.typeName.lower().find('resistor') != -1:
				print 'res'
				dc.SetPen(wx.Pen(wx.Color(255,0,0),5))
				points = []
				resLength = 50
				resHeight = 20
				startL = float(totalLength-resLength )/ 2
				startX = x1 + (startL*slopeX)
				startY =y1 + (startL*slopeY)
				endX = startX+(resLength*slopeX)
				endY = startY+(resHeight*slopeY)	
				points.append((startX-15,startY)) #top left vertices
				points.append((startX+15,startY)) #top right vertices
				points.append((endX+15,endY)) #top right vertices

				points.append((endX-15,endY)) #top left vertices
				
				dc.DrawPolygon(points)
			
			
			
class VariableBreadboardComponentWrapper:
	"""this needed to happen"""
	def __init__(self,breadboardPanel,variableBreadboardComponent):
		self.bbp = breadboardPanel
		self.vbbc = variableBreadboardComponent
		self.typeName= type(self.vbbc).__name__
		
		#main image of this component's center
		if not self.typeName in self.bbp.typeToImage.keys():
			self.bbp.loadTypeImage(self.typeName)
		#image of the wire....
		if not BreadboardPanel.PLAINWIRE in self.bbp.typeToImage.keys():
			self.bbp.loadTypeImage(BreadboardPanel.PLAINWIRE)
		
		self.mainBMP = None #will be created on first draw
		self.wireBMP = None #will be created on first draw


	def getTheta(self,dx,dy):
		print dx,dy
		if dx ==0:
			if dy > 0:
				return 90
			else:
				return -90
		if dy ==0:
			if dx >0:
				return 180
			else:
				return 0
		if dy <0 and dx >0:
			res = (180-math.degrees(math.atan(dy/dx)))
			print res
			return res
		if dy >0 and dx >0:
			return 180.0- math.degrees(math.atan(dy/dx))
		return -math.degrees(math.atan(dy/dx))

	def drawSelf(self,dc,rescale):
		"""draw this vbbc. optionally, if xy1 and xy2 are non None, draw it between the two XY's,
		 instead of the locations, which may not be absolute"""		
		x1,y1 = self.bbp.getCenteredXY(self.vbbc.pinList[0].getLocationTuple())
		x2,y2 = self.bbp.getCenteredXY(self.vbbc.pinList[1].getLocationTuple())		
		dx,dy = (x1-x2,y1-y2)
		disp = self.vbbc.pinList[0].displacementTo(self.vbbc.pinList[1])
		totalLength = math.sqrt(dx**2 +dy**2)
		slopeX = dx/totalLength
		slopeY = dy/totalLength #slope of x with respect to length	

		dc.SetPen( wx.Pen( wx.Color(128,128,128),3))
		dc.DrawLine(x1,y1,x2,y2)
		if self.typeName.lower().find('wire') != -1:
			dc.SetPen(wx.Pen(wx.Color(255,0,0),5))
			startX=x1 + (0.1*totalLength*slopeX)
			startY =y1 + (0.1*totalLength*slopeY)
			endX = startX+(0.8*totalLength*slopeX)
			endY = startY+(0.8*totalLength*slopeY)	
			dc.DrawLine(startX,startY,endX,endY)
		elif self.typeName.lower().find('resistor') != -1:
			imgFilename ='res/components/plainwire_image.png'
			self.pilImage = Image.open( imgFilename )
			self.pilImage.save('part1.png')
			#twice the length is used, as the images are half length
			self.pilImage = self.pilImage.resize((int(totalLength)*2,self.pilImage.size[1]))
			self.pilImage.save('part2.png')
			rotatedPilImage = self.pilImage.rotate(self.getTheta(dx,dy),Image.BICUBIC, expand=True )
			rotated_wxImage = ImgConv.WxImageFromPilImage( rotatedPilImage )
			imageWid, imageHgt = rotated_wxImage.GetSize()
			offsetX = (x1) -(imageWid / 2)
			offsetY = (y1) - (imageHgt / 2)
			# Display the rotated image. Only wxBitmaps can be displayed, not wxImages.
			# .DrawBitmap() autmatically "closes" the dc, meaning it finalizes the bitmap in some way.
			dc.DrawBitmap( rotated_wxImage.ConvertToBitmap(), offsetX, offsetY)


			
			
		
class FixedBreadboardComponentWrapper:
	def __init__(self,breadboardPanel,fixedBreadboardComponent):
		self.bbp = breadboardPanel
		self.fbbc = fixedBreadboardComponent
		self.typeName= type(self.fbbc).__name__
		if not self.typeName in self.bbp.typeToImage.keys():
			self.bbp.loadTypeImage(self.typeName,instance=self.fbbc)
		self.pos = None

	def drawSelf(self,dc,rescale):
		if rescale or self.bbp.typeToBitmap[self.typeName] == None:
			self.bbp.typeToBitmap[self.typeName] = copy.copy(self.bbp.typeToImage[self.typeName]).Rescale(self.bbp.bmpW*self.fbbc.width,self.bbp.bmpH*self.fbbc.height,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
			if self.pos != None:
				self.bmp = copy.copy(self.bbp.typeToBitmap[self.typeName]) #store a local copy for blitting	
		if self.pos != None:
			self.drawMovingSelf(dc)
		x,y = self.bbp.getXY(self.fbbc.pinList[0].getLocationTuple())
		y -= self.bbp.bmpH * (self.fbbc.height -1)
		dc.DrawBitmap(self.bbp.typeToBitmap[self.typeName], x, y)
	
		
	def drawMovingSelf(self,dc):
		op = wx.COPY
		if self.bmp.Ok():
			memDC = wx.MemoryDC()
			memDC.SelectObject(self.bmp1)
			dc.Blit(self.pos[0], self.pos[1]-(self.breadboardComponent.height*bmpH),self.bmp1.GetWidth(), self.bmp1.GetHeight(),memDC, 0, 0, op, True)

class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent, title=title)
		bb = Breadboard()		
		a = OpAmp('hello')
		c = Resistor(10)
		print bb.putComponent(c,28,10,8,4)
		print bb.putComponent(a,8,7)
		BreadboardPanel(self,bb)
		self.Fit()
		self.Show()

if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
