import wx
import wx.aui
from BreadboardPanel import *
class BreadboardGUI(wx.Frame):
	def __init__(self, parent, id=-1, title='wx.aui Test',
				 pos=wx.DefaultPosition, size=(900, 400),
				 style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		self._mgr = wx.aui.AuiManager(self)

		# create several text controls
		self.breadBoardPanel = BreadboardPanel(self,Breadboard())

		self.partBrowserPanel = wx.TextCtrl(self, -1, 'Part Browser Panel!',
							wx.DefaultPosition, wx.Size(200,80),
							wx.NO_BORDER | wx.TE_MULTILINE)

		text3 = wx.TextCtrl(self, -1, 'History Panel?',
							wx.DefaultPosition, wx.Size(200,150),
							wx.NO_BORDER | wx.TE_MULTILINE)

		# add the panes to the manager
		self._mgr.AddPane(self.breadBoardPanel, wx.CENTER) #main focused widget
		self._mgr.AddPane(self.partBrowserPanel, wx.BOTTOM, 'Part Browser')
		self._mgr.AddPane(text3, wx.RIGHT, 'Simulation Toolbar?')

		# tell the manager to 'commit' all the changes just made
		self._mgr.Update()

		self.Bind(wx.EVT_CLOSE, self.OnClose)


	def OnClose(self, event):
		# deinitialize the frame manager
		self._mgr.UnInit()
		# delete the frame
		self.Destroy()


app = wx.App()
frame = BreadboardGUI(None)
frame.Show()
app.MainLoop()
