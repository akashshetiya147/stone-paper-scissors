import wx


def show_stats_dialog(parent, choice_stats, player_name="Player"):
    """Display win probability statistics for each choice."""
    
    dialog = wx.Dialog(parent, title=f"{player_name}'s Stats", size=(600, 450))
    panel = wx.Panel(dialog)
    sizer = wx.BoxSizer(wx.VERTICAL)
    
    # Title
    title = wx.StaticText(panel, label=f"{player_name}'s Win Probability")
    title.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    sizer.Add(title, 0, wx.ALL | wx.CENTER, 15)
    
    # Colors for each choice
    colors = {
        'Rock': wx.Colour(255, 0, 0),
        'Paper': wx.Colour(0, 100, 255),
        'Scissors': wx.Colour(0, 255, 100)
    }
    
    # Calculate and display stats
    stats_text = []
    bars = []
    
    for choice in ['Rock', 'Paper', 'Scissors']:
        trials = choice_stats[choice]['trials']
        wins = choice_stats[choice]['wins']
        win_rate = (wins / trials) * 100 if trials > 0 else 33.33
        
        stats_text.append(f"{choice}: {win_rate:.1f}%")
        bars.append((choice, win_rate, colors[choice]))
    
    # Display text stats
    text = wx.StaticText(panel, label="\n".join(stats_text))
    text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    sizer.Add(text, 0, wx.ALL | wx.CENTER, 10)
    
    # Bar chart
    chart_panel = wx.Panel(panel, size=(500, 250))
    chart_sizer = wx.BoxSizer(wx.HORIZONTAL)
    
    for choice, win_rate, color in bars:
        bar_box = wx.BoxSizer(wx.VERTICAL)
        bar_box.AddStretchSpacer()
        
        # Bar height (max 200px)
        bar_height = max(5, int((win_rate / 100) * 200))
        bar = wx.Panel(chart_panel, size=(80, bar_height))
        bar.SetBackgroundColour(color)
        bar_box.Add(bar, 0, wx.ALIGN_CENTER)
        
        # Label
        label = wx.StaticText(chart_panel, label=f"{choice}\n{win_rate:.1f}%")
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        bar_box.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        
        chart_sizer.Add(bar_box, 0, wx.ALL | wx.EXPAND, 15)
    
    chart_panel.SetSizer(chart_sizer)
    sizer.Add(chart_panel, 1, wx.ALL | wx.CENTER | wx.EXPAND, 10)
    
    # Best choice insight
    best = max(bars, key=lambda x: x[1])
    if best[1] > 33.33:
        insight = wx.StaticText(panel, label=f"💡 Best choice: {best[0]} ({best[1]:.1f}%)")
        insight.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        insight.SetForegroundColour(wx.Colour(0, 150, 0))
        sizer.Add(insight, 0, wx.ALL | wx.CENTER, 10)
    
    # Close button
    close_btn = wx.Button(panel, wx.ID_CLOSE, "Close")
    close_btn.Bind(wx.EVT_BUTTON, lambda e: dialog.Close())
    sizer.Add(close_btn, 0, wx.ALL | wx.CENTER, 10)
    
    panel.SetSizer(sizer)
    dialog.ShowModal()
    dialog.Destroy()