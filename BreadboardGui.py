import wx
import wx.aui
from BreadboardPanel import *
from SimulationPanel import *
from PartBrowserPanel import *
from ComponentEditorPanel import *
from B2Spice import *
import randomplotter

class BreadboardGUI(wx.Frame):
	def __init__(self, parent,breadboard, *args, **kwargs):
		wx.Frame.__init__(self, parent,size=(1200,400),pos=wx.DefaultPosition,*args,**kwargs)
		self._mgr = wx.aui.AuiManager(self)
		# create menu
		self.createMenu()
		self.partBrowserPanel = PartBrowserPanel(self)
		self.breadboard = breadboard
		self.breadboardPanel = BreadboardPanel(self,self.breadboard,self.partBrowserPanel.buttonGroup)
		self.simulationPanel = SimulationPanel(self)
		# add the panes to the manager

		auiInfo =  wx.aui.AuiPaneInfo().Bottom().CaptionVisible(False)
		auiInfo.dock_proportion = 0
		auiInf1 =  wx.aui.AuiPaneInfo().Center().CaptionVisible(False)
		auiInf1.dock_proportion = 0
		self._mgr.AddPane(self.breadboardPanel,auiInf1) #main focused widget
		self._mgr.AddPane(self.partBrowserPanel,auiInfo)
		self._mgr.AddPane(self.simulationPanel, wx.RIGHT)

		self.Layout()
		self._mgr.Update()
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.simulationPanel.Bind(wx.EVT_BUTTON,self.OnSimulateButtonPress)

	def createMenu(self):
		filemenu= wx.Menu()
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open","Generic open")
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		
		menuSave = filemenu.Append(wx.ID_SAVE, "&Save","Generic save")
		self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
		menuAbout= filemenu.Append(wx.ID_ABOUT, "&About","Generic Information about this program")
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
				
		menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Get Minched")
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        # Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

	def OnExit(self,event):
		print "on exit event, I killed the frame..."
		self.OnClose(event) #for now, terminate frame
	
	def OnOpen(self,event):
		dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = os.path.join(self.dirname, self.filename)
			self.breadboard = Breadboard.openBreadboard(f)
		dlg.Destroy()
		print "hmm"
		print id(self.breadboard),id(self.breadboardPanel.breadboard)
		self.breadboardPanel.breadboard = self.breadboard
		self.breadboardPanel.killCurrent()
		self.breadboardPanel.Refresh()
		self.breadboardPanel.Update()
		
	def OnSave(self,event):
		dlg = wx.FileDialog(self, "Save this circuit", os.getcwd(), "", "*.*", wx.SAVE |wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = os.path.join(self.dirname, self.filename)
			self.breadboard.saveBreadboard(f)
			if os.path.exists(f):
				print "successfully saved"
		dlg.Destroy()
		
	def OnAbout(self,event):
		# Create a message dialog box
		dlg = wx.MessageDialog(self, str(self.breadboard.componentList), "About Sample Editor", wx.OK)
		dlg.ShowModal() # Shows it
		dlg.Destroy() # finally destroy it when finished.

	def OnClose(self, event):
		# deinitialize the frame manager
		self._mgr.UnInit()
		# delete the frame
		self.Destroy()
		
	def OnSimulateButtonPress(self,event):
		
		simType = self.simulationPanel.comboBox.GetValue()
		b = B2Spice(self.breadboard)
		if simType.find('AC') != -1:
			print 'AC'
			b.buildNetList('ac')
		elif simType.find('Transient') != -1:
			print 'Transient'
			b.buildNetList('tran')
		elif simType.find('DC') != -1:
			print 'Transient'
			b.buildNetList('tran')
		else:
			print "no mode of analysis"


if __name__=="__main__":

		bb = Breadboard()		
		a = OpAmp()
		c = Resistor(10)

		bb.putComponent(c,28,10,8,4)
		bb.putComponent(a,17,13)
		app = wx.App()
		frame = BreadboardGUI(None,bb)
		frame.Show()
		app.MainLoop()
