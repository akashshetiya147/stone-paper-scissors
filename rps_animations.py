import wx
import math


def show_animated_choices_parallel(panel, result_texts, choice1, choice2, player1="Player 1", player2="Player 2"):
    """
    Display animated hand signs for both players showing their choices.
    
    Args:
        panel: The wx.Panel to draw on
        result_texts: List to append created UI elements for cleanup
        choice1: First player's choice ("Rock", "Paper", or "Scissors")
        choice2: Second player's choice ("Rock", "Paper", or "Scissors")
        player1: First player's name (default: "Player 1")
        player2: Second player's name (default: "Player 2")
    """
    
    # Map choices to emoji hand signs
    choice_to_emoji = {
        "Rock": "✊",
        "Paper": "✋",
        "Scissors": "✌️"
    }
    
    # Clear any previous animation elements
    emojis = ["✊", "✋", "✌️"]
    for item in result_texts[:]:
        try:
            if isinstance(item, wx.Panel):
                item.Destroy()
                result_texts.remove(item)
            elif isinstance(item, wx.StaticText) and item.GetLabel() in emojis:
                item.Destroy()
                result_texts.remove(item)
        except Exception:
            pass
    
    # Create dark background panels for the animation
    bg_panel1 = wx.Panel(panel, pos=(350, 450), size=(200, 150))
    bg_panel1.SetBackgroundColour(wx.Colour(20, 20, 30, 220))
    result_texts.append(bg_panel1)
    
    bg_panel2 = wx.Panel(panel, pos=(700, 450), size=(200, 150))
    bg_panel2.SetBackgroundColour(wx.Colour(20, 20, 30, 220))
    result_texts.append(bg_panel2)
    
    # Get emojis for the choices
    emoji1 = choice_to_emoji.get(choice1, "✊")
    emoji2 = choice_to_emoji.get(choice2, "✊")
    
    # Create hand sign displays
    hand_font = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    
    # Player 1 label
    player1_label = wx.StaticText(panel, label=player1, pos=(380, 455))
    player1_label.SetFont(label_font)
    player1_label.SetForegroundColour(wx.Colour(1, 135, 255))
    result_texts.append(player1_label)
    
    # Player 1 hand sign
    hand1 = wx.StaticText(panel, label=emoji1, pos=(410, 490))
    hand1.SetFont(hand_font)
    hand1.SetForegroundColour(wx.Colour(1, 135, 255))
    result_texts.append(hand1)
    
    # Player 2 label
    player2_label = wx.StaticText(panel, label=player2, pos=(730, 455))
    player2_label.SetFont(label_font)
    player2_label.SetForegroundColour(wx.RED)
    result_texts.append(player2_label)
    
    # Player 2 hand sign
    hand2 = wx.StaticText(panel, label=emoji2, pos=(760, 490))
    hand2.SetFont(hand_font)
    hand2.SetForegroundColour(wx.RED)
    result_texts.append(hand2)
    
    panel.Update()
    wx.MilliSleep(500)  # Show the choices for half a second


def animate_countdown(panel, result_texts):
    """
    Display a countdown animation (Rock! Paper! Scissors! Shoot!)
    
    Args:
        panel: The wx.Panel to draw on
        result_texts: List to append created UI elements for cleanup
    """
    countdown_words = ["Rock!", "Paper!", "Scissors!", "Shoot!"]
    countdown_font = wx.Font(40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    
    for word in countdown_words:
        # Clear previous countdown text
        for item in result_texts[:]:
            if isinstance(item, wx.StaticText) and item.GetLabel() in countdown_words:
                item.Destroy()
                result_texts.remove(item)
        
        # Create new countdown text
        countdown_text = wx.StaticText(panel, label=word, pos=(550, 400))
        countdown_text.SetFont(countdown_font)
        countdown_text.SetForegroundColour(wx.Colour(255, 255, 0))
        result_texts.append(countdown_text)
        
        panel.Update()
        wx.MilliSleep(500)
    
    # Clear the "Shoot!" text after a moment
    wx.MilliSleep(300)
    for item in result_texts[:]:
        if isinstance(item, wx.StaticText) and item.GetLabel() in countdown_words:
            item.Destroy()
            result_texts.remove(item)


def create_animated_vs_display(panel, result_texts, player1="Player 1", player2="Player 2"):
    """
    Create a "VS" display between two players with animation effect.
    
    Args:
        panel: The wx.Panel to draw on
        result_texts: List to append created UI elements for cleanup
        player1: First player's name
        player2: Second player's name
    """
    vs_font = wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    name_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    
    # Player 1 name
    p1_text = wx.StaticText(panel, label=player1, pos=(350, 300))
    p1_text.SetFont(name_font)
    p1_text.SetForegroundColour(wx.Colour(1, 135, 255))
    result_texts.append(p1_text)
    
    # VS text
    vs_text = wx.StaticText(panel, label="VS", pos=(580, 280))
    vs_text.SetFont(vs_font)
    vs_text.SetForegroundColour(wx.Colour(255, 215, 0))  # Gold color
    result_texts.append(vs_text)
    
    # Player 2 name
    p2_text = wx.StaticText(panel, label=player2, pos=(750, 300))
    p2_text.SetFont(name_font)
    p2_text.SetForegroundColour(wx.RED)
    result_texts.append(p2_text)
    
    panel.Update()
    wx.MilliSleep(1000)


def pulse_animation(widget, duration_ms=500, steps=10):
    """
    Create a pulsing effect on a widget by changing its size.
    
    Args:
        widget: The wx widget to animate
        duration_ms: Total duration of the animation in milliseconds
        steps: Number of steps in the animation
    """
    original_size = widget.GetSize()
    delay = duration_ms // (steps * 2)  # Half for grow, half for shrink
    
    # Grow phase
    for i in range(1, steps + 1):
        scale = 1 + (0.2 * i / steps)  # Scale up to 1.2x
        new_width = int(original_size.width * scale)
        new_height = int(original_size.height * scale)
        widget.SetSize(new_width, new_height)
        wx.MilliSleep(delay)
        widget.Update()
    
    # Shrink phase
    for i in range(steps, 0, -1):
        scale = 1 + (0.2 * i / steps)
        new_width = int(original_size.width * scale)
        new_height = int(original_size.height * scale)
        widget.SetSize(new_width, new_height)
        wx.MilliSleep(delay)
        widget.Update()
    
    # Restore original size
    widget.SetSize(original_size)


def shake_animation(widget, duration_ms=300, intensity=5):
    """
    Create a shaking effect on a widget by moving it back and forth.
    
    Args:
        widget: The wx widget to animate
        duration_ms: Total duration of the animation in milliseconds
        intensity: Pixel distance to shake
    """
    original_pos = widget.GetPosition()
    steps = 10
    delay = duration_ms // steps
    
    for i in range(steps):
        offset_x = intensity if i % 2 == 0 else -intensity
        new_pos = (original_pos.x + offset_x, original_pos.y)
        widget.SetPosition(new_pos)
        wx.MilliSleep(delay)
        widget.Update()
    
    # Restore original position
    widget.SetPosition(original_pos)


def fade_in_text(panel, result_texts, text, pos, font, color, duration_ms=500):
    """
    Create a fade-in effect for text by gradually increasing opacity.
    Note: wx.StaticText doesn't support transparency well, so we simulate with color intensity.
    
    Args:
        panel: The wx.Panel to draw on
        result_texts: List to append created UI elements
        text: Text to display
        pos: Position tuple (x, y)
        font: wx.Font to use
        color: Final wx.Colour
        duration_ms: Duration of fade in milliseconds
    
    Returns:
        The created wx.StaticText widget
    """
    text_widget = wx.StaticText(panel, label=text, pos=pos)
    text_widget.SetFont(font)
    
    steps = 10
    delay = duration_ms // steps
    
    for i in range(1, steps + 1):
        intensity = i / steps
        fade_color = wx.Colour(
            int(color.Red() * intensity),
            int(color.Green() * intensity),
            int(color.Blue() * intensity)
        )
        text_widget.SetForegroundColour(fade_color)
        wx.MilliSleep(delay)
        text_widget.Update()
    
    text_widget.SetForegroundColour(color)
    result_texts.append(text_widget)
    return text_widget
