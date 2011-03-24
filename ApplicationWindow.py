from wxPython.wx import *

class ApplicationWindow(wxApp):
    def OnInit(self):
        frame = wxFrame(NULL, -1, "Minch's Magic Storey Land")
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

app = ApplicationWindow(0)
app.MainLoop()
