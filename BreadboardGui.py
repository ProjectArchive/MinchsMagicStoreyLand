import wx
import wx.aui
from BreadboardPanel import *
from SimulationPanel import *
class BreadboardGUI(wx.Frame):
	def __init__(self, parent,breadBoard, *args, **kwargs):
		wx.Frame.__init__(self, parent,*args,**kwargs)
		self._mgr = wx.aui.AuiManager(self)
		# create several text controls
		self.breadBoardPanel = BreadboardPanel(self,breadBoard)

		self.partBrowserPanel = wx.TextCtrl(self, -1, 'Part Browser Panel!',
							wx.DefaultPosition, wx.Size(400,120),
							wx.NO_BORDER | wx.TE_MULTILINE)

		text3 = SimulationPanel(self,size=(400,100))

		# add the panes to the manager
		self._mgr.AddPane(self.breadBoardPanel, wx.CENTER) #main focused widget
		self._mgr.AddPane(self.partBrowserPanel, wx.BOTTOM, 'Part Browser')
		self._mgr.AddPane(text3, wx.RIGHT, 'Simulation Toolbar')

		# tell the manager to 'commit' all the changes just made
		self._mgr.Update()

		self.Bind(wx.EVT_CLOSE, self.OnClose)


	def OnClose(self, event):
		# deinitialize the frame manager
		self._mgr.UnInit()
		# delete the frame
		self.Destroy()


app = wx.App()
frame = BreadboardGUI(None,Breadboard(),size=(900,400))
frame.Show()
app.MainLoop()
