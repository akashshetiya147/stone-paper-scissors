import wx


class NameInputDialog(wx.Dialog):
    """Dialog to get player names based on game mode"""
    
    def __init__(self, parent, is_two_player=False):
        super().__init__(parent, title="Enter Player Names", size=(400, 250) if is_two_player else (400, 200))
        self.is_two_player = is_two_player
        self.player1_name = None
        self.player2_name = None
        
        self.init_ui()
        self.Centre()
    
    def init_ui(self):
        """Initialize the UI"""
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        if self.is_two_player:
            title = wx.StaticText(panel, label="Enter Player Names")
        else:
            title = wx.StaticText(panel, label="Enter Your Name")
        
        title.SetFont(title_font)
        sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        
        # Player 1 name
        label1 = wx.StaticText(panel, label="Player 1 Name:" if self.is_two_player else "Your Name:")
        self.player1_text = wx.TextCtrl(panel, size=(300, -1))
        
        sizer.Add(label1, 0, wx.LEFT | wx.TOP, 15)
        sizer.Add(self.player1_text, 0, wx.LEFT | wx.RIGHT, 15)
        
        # Player 2 name (only for two-player mode)
        if self.is_two_player:
            label2 = wx.StaticText(panel, label="Player 2 Name:")
            self.player2_text = wx.TextCtrl(panel, size=(300, -1))
            
            sizer.Add(label2, 0, wx.LEFT | wx.TOP, 15)
            sizer.Add(self.player2_text, 0, wx.LEFT | wx.RIGHT, 15)
        
        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ok_btn = wx.Button(panel, wx.ID_OK, "OK", size=(80, 30))
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "Cancel", size=(80, 30))
        
        button_sizer.Add(ok_btn, 0, wx.RIGHT, 10)
        button_sizer.Add(cancel_btn, 0, wx.RIGHT, 0)
        
        sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 15)
        
        # Bind events
        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
        
        panel.SetSizer(sizer)
    
    def on_ok(self, event):
        """Handle OK button"""
        self.player1_name = self.player1_text.GetValue().strip()
        
        if not self.player1_name:
            wx.MessageBox("Please enter a name!", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if self.is_two_player:
            self.player2_name = self.player2_text.GetValue().strip()
            
            if not self.player2_name:
                wx.MessageBox("Please enter both names!", "Error", wx.OK | wx.ICON_ERROR)
                return
        
        self.EndModal(wx.ID_OK)
    
    def on_cancel(self, event):
        """Handle Cancel button"""
        self.EndModal(wx.ID_CANCEL)
    
    def get_names(self):
        """Get the entered names"""
        if self.is_two_player:
            return self.player1_name, self.player2_name
        else:
            return self.player1_name


def show_name_input(parent, is_two_player=False):
    """Show the name input dialog and return the names"""
    dialog = NameInputDialog(parent, is_two_player)
    
    if dialog.ShowModal() == wx.ID_OK:
        names = dialog.get_names()
        dialog.Destroy()
        return names
    else:
        dialog.Destroy()
        return None
