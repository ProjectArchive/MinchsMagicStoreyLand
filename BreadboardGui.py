import wx
import wx.aui
from BreadboardPanel import *
from SimulationPanel import *
from PartBrowserPanel import *

class BreadboardGUI(wx.Frame):
	def __init__(self, parent,breadBoard, *args, **kwargs):
		wx.Frame.__init__(self, parent,*args,**kwargs)
		self._mgr = wx.aui.AuiManager(self)
		# create menu
		self.createMenu()
		
		self.breadBoardPanel = BreadboardPanel(self,breadBoard)

		self.partBrowserPanel = PartBrowserPanel(self)

		text3 = SimulationPanel(self)

		# add the panes to the manager

		self._mgr.AddPane(self.breadBoardPanel,wx.CENTER) #main focused widget
		self._mgr.AddPane(self.partBrowserPanel, wx.BOTTOM)
		self._mgr.AddPane(text3, wx.RIGHT, 'Simulation Toolbar')

		# tell the manager to 'commit' all the changes just made
		self.Fit()
		self._mgr.Update()
		

		self.Bind(wx.EVT_CLOSE, self.OnClose)
	
	def createMenu(self):
		filemenu= wx.Menu()
		
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open","Generic open")
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		
		menuAbout= filemenu.Append(wx.ID_ABOUT, "&About","Generic Information about this program")
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
				
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Get Minched")
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        # Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

	def OnExit(self,event):
		print "on exit event, I killed the frame..."
		self.OnClose(event) #for now, terminate frame
	
	def OnOpen(self,event):
		print "on open event....we should do something"
		
	def OnAbout(self,event):
		print "Something about me..."

	def OnClose(self, event):
		# deinitialize the frame manager
		self._mgr.UnInit()
		# delete the frame
		self.Destroy()



app = wx.App()
frame = BreadboardGUI(None,Breadboard())
frame.Show()
app.MainLoop()