from pickle import FALSE

import wx
import random
from CSVFORSTORE import *
import math
from name_input import show_name_input
import winsound
from stats import show_stats_dialog
import os
import wave
import struct



# --- Transparent Text Class ---
class TransparentText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
        super().__init__(parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def on_size(self, event):
        self.Refresh()
        event.Skip()


# --- Hexagon Neon Button Class ---
class HexagonNeonButton(wx.Window):
    def __init__(self, parent, label='', neon_color=wx.Colour(255, 0, 0), pos=wx.DefaultPosition, size=(120, 120), colors=None):
        super().__init__(parent, pos=pos, size=size, style=wx.TRANSPARENT_WINDOW)
        self.label = label
        self.neon_color = neon_color
        self.colors = colors  # For multi-colored buttons like Random
        self.is_hovered = False
        self.is_enabled = True
        self.click_callback = None
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GCDC(dc)
        
        width, height = self.GetSize()
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 5
        
        # Draw hexagon
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append(wx.Point(int(x), int(y)))
        
        # Determine if this is a multi-colored button
        is_multicolor = self.colors is not None and len(self.colors) > 1
        
        # Handle multi-colored hexagon (for Random button)
        if is_multicolor:
            # Draw each colored sector (1/3 of hexagon = 2 sides)
            for sector in range(3):
                sector_color = self.colors[sector]
                # Get the 2 points for this sector plus center
                idx1 = sector * 2
                idx2 = (sector * 2 + 1) % 6
                idx3 = (sector * 2 + 2) % 6
                
                sector_points = [
                    wx.Point(center_x, center_y),
                    points[idx1],
                    points[idx2],
                    points[idx3]
                ]
                
                # Draw glow for this sector
                for glow in range(2, 0, -1):
                    glow_color = wx.Colour(
                        int(sector_color.Red() * (0.5 + 0.5 * (3 - glow) / 3) if self.is_hovered else sector_color.Red() * 0.5),
                        int(sector_color.Green() * (0.5 + 0.5 * (3 - glow) / 3) if self.is_hovered else sector_color.Green() * 0.5),
                        int(sector_color.Blue() * (0.5 + 0.5 * (3 - glow) / 3) if self.is_hovered else sector_color.Blue() * 0.5)
                    )
                    gc.SetPen(wx.Pen(glow_color, glow))
                    gc.SetBrush(wx.Brush(glow_color))
                    gc.DrawPolygon(sector_points)
                
                # Draw main sector color
                main_color = wx.Colour(
                    min(255, int(sector_color.Red() * (1.5 if self.is_hovered else 0.7))),
                    min(255, int(sector_color.Green() * (1.5 if self.is_hovered else 0.7))),
                    min(255, int(sector_color.Blue() * (1.5 if self.is_hovered else 0.7)))
                )
                gc.SetPen(wx.Pen(main_color, 2 if self.is_hovered else 1))
                gc.SetBrush(wx.Brush(wx.Colour(30, 30, 40)))
                gc.DrawPolygon(sector_points)
        else:
            # Single color hexagon (original logic)
            # Set color based on hover state
            if self.is_hovered:
                # Bright neon when hovered
                border_color = wx.Colour(
                    min(255, int(self.neon_color.Red() * 1.5)),
                    min(255, int(self.neon_color.Green() * 1.5)),
                    min(255, int(self.neon_color.Blue() * 1.5))
                )
                border_width = 4
                glow_width = 6
                text_brightness = 1.5
            else:
                # Dull neon when not hovered
                border_color = wx.Colour(
                    max(50, int(self.neon_color.Red() * 0.5)),
                    max(50, int(self.neon_color.Green() * 0.5)),
                    max(50, int(self.neon_color.Blue() * 0.5))
                )
                border_width = 2
                glow_width = 2
                text_brightness = 0.7
            
            # Draw glow effect
            for i in range(glow_width, 0, -1):
                glow_color = wx.Colour(
                    int(border_color.Red() * (0.5 + 0.5 * (glow_width - i) / glow_width)),
                    int(border_color.Green() * (0.5 + 0.5 * (glow_width - i) / glow_width)),
                    int(border_color.Blue() * (0.5 + 0.5 * (glow_width - i) / glow_width))
                )
                gc.SetPen(wx.Pen(glow_color, i))
                gc.DrawPolygon(points)
            
            # Draw main hexagon border
            gc.SetPen(wx.Pen(border_color, border_width))
            gc.SetBrush(wx.Brush(wx.Colour(30, 30, 40, 200)))
            gc.DrawPolygon(points)
        
        # Draw label
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font)
        
        # Text color based on hover state
        if is_multicolor:
            # Use white for multi-color buttons
            text_color = wx.Colour(255, 255, 255)
        else:
            text_color = wx.Colour(
                min(255, int(self.neon_color.Red() * (1.5 if self.is_hovered else 0.7))),
                min(255, int(self.neon_color.Green() * (1.5 if self.is_hovered else 0.7))),
                min(255, int(self.neon_color.Blue() * (1.5 if self.is_hovered else 0.7)))
            )
        gc.SetTextForeground(text_color)
        
        # Measure text to center it
        text_width, text_height = gc.GetTextExtent(self.label)
        text_x = center_x - text_width // 2
        text_y = center_y - text_height // 2
        
        gc.DrawText(self.label, int(text_x), int(text_y))

    def on_click(self, event):
        if self.is_enabled and self.click_callback:
            try:
                play_click_sound()
            except Exception:
                pass
            self.click_callback(event)

    def on_enter(self, event):
        self.is_hovered = True
        self.Refresh()

    def on_leave(self, event):
        self.is_hovered = False
        self.Refresh()

    def on_size(self, event):
        self.Refresh()

    def Bind(self, event_type, handler):
        if event_type == wx.EVT_BUTTON:
            self.click_callback = handler
        else:
            super().Bind(event_type, handler)

    def Enable(self, enable=True):
        self.is_enabled = enable
        self.Refresh()

    def Hide(self):
        super().Hide()

    def Show(self, show=True):
        super().Show(show)

    def SetLabel(self, label):
        self.label = label
        self.Refresh()


# --- GAME VARIABLES ---
player1 = "User"
player2 = "Bot"
is_two_player = False
player1_choice = None
player2_choice = None
waiting_for_player2 = False

s = 0
x = 0
ranusch = 0
botchoicein = 0
round_count = 0
max_rounds = 5
result_texts = []

# Stats tracking: trials and wins per user choice (for player1)
choice_stats = {
    'Rock': {'trials': 0, 'wins': 0},
    'Paper': {'trials': 0, 'wins': 0},
    'Scissors': {'trials': 0, 'wins': 0}
}


def ensure_minecraft_sound():
    """Generate a short 'F1 radio' like WAV if it doesn't exist."""
    sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    path = os.path.join(sounds_dir, 'f1_radio.wav')
    if os.path.isfile(path):
        return path

    # Synth parameters: short FM/chirp + subtle noise to mimic radio button sound
    framerate = 44100
    duration = 0.20
    nframes = int(framerate * duration)
    amplitude = 14000

    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        for i in range(nframes):
            t = i / framerate
            # frequency sweep from ~800Hz up to ~3500Hz
            freq = 800 + 2700 * (t / duration)
            carrier = math.sin(2 * math.pi * freq * t)

            # add subtle FM modulation
            fm = math.sin(2 * math.pi * (freq * 0.5) * t) * 0.3
            sample = carrier * (1 + fm)

            # add short burst of filtered noise for radio texture
            noise = (random.random() * 2 - 1) * math.exp(-8 * t)
            value = amplitude * (0.8 * sample + 0.2 * noise) * math.exp(-6 * t)

            packed = struct.pack('<h', int(max(-32767, min(32767, value))))
            wf.writeframes(packed)

    return path


_CLICK_SOUND_PATH = None

def play_click_sound():
    """Play the generated minecraft-like button sound asynchronously."""
    global _CLICK_SOUND_PATH
    try:
        if _CLICK_SOUND_PATH is None:
            _CLICK_SOUND_PATH = ensure_minecraft_sound()
        winsound.PlaySound(_CLICK_SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass


def botgame():
    global player1, player2, is_two_player
    
    # Get player name from dialog
    result = show_name_input(mainwin, is_two_player=False)
    if result is None:  # User cancelled
        return
    
    player1 = result
    player2 = "Bot"
    is_two_player = False
    restart_game(None)

    pvp.Hide()
    bot_btn.Hide()
    stone.Show()
    paper.Show()
    scissors.Show()
    Rand.Show()
    stats_btn.Show()

    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)
    clear_result_texts()


def twoplayergame():
    global player1, player2, is_two_player
    
    # Get player names from dialog
    result = show_name_input(mainwin, is_two_player=True)
    if result is None:  # User cancelled
        return
    
    player1, player2 = result
    is_two_player = True
    restart_game(None)
    # Hide mode selection buttons
    pvp.Hide()
    bot_btn.Hide()
    # Show and enable game buttons
    stone.Show()
    paper.Show()
    scissors.Show()
    Rand.Show()
    stats_btn.Show()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)
    clear_result_texts()


def botchoice():
    global botchoicein
    botchoicein = random.randint(0, 2)


def randomuserchoice(event):
    global ranusch
    ranusch = random.randint(0, 2)
    choice = ["Rock", "Paper", "Scissors"]
    play_round(choice[ranusch])


def clear_result_texts():
    global result_texts
    for text in result_texts:
        text.Destroy()
    result_texts = []


def show_animated_choices_parallel(choice1, choice2):
    """Removed hand-sign animation and static display — no UI is created.

    This function now only removes any previously-created dark background panels
    or hand-sign StaticText entries from `result_texts` so nothing is shown.
    """
    emojis = ["✊", "✋", "✌️"]

    # Destroy any lingering dark panels or emoji StaticText entries
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

    panel.Update()
    return


def show_game_over():
    clear_result_texts()

    large_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    medium_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

    game_over_text = TransparentText(panel, label="GAME OVER!", pos=(550, 350))
    game_over_text.SetFont(large_font)
    game_over_text.SetForegroundColour(wx.Colour(255, 0, 0))
    result_texts.append(game_over_text)

    if s > x:
        winner_text = TransparentText(panel, label=f"{player1} WINS!  Final Score - {player1}: {s}, {player2}: {x}",pos=(450, 400))
        winner_text.SetForegroundColour(wx.Colour(1, 135, 255))
    elif x > s:
        winner_text = TransparentText(panel, label=f"{player2} WINS! Final Score - {player1}: {s}, {player2}: {x}",pos=(450, 400))
        winner_text.SetForegroundColour(wx.RED)
    else:
        winner_text = TransparentText(panel, label=f"IT'S A TIE! Final Score - {player1}: {s}, {player2}: {x}",pos=(450, 400))
        winner_text.SetForegroundColour(wx.Colour(171, 1, 255))

    winner_text.SetFont(medium_font)
    result_texts.append(winner_text)

    restart_btn = wx.Button(panel, label="Restart Game", size=(120, 40), pos=(510, 450))
    def _restart_click(e):
        try:
            play_click_sound()
        except Exception:
            pass
        restart_game(e)
    restart_btn.Bind(wx.EVT_BUTTON, _restart_click)
    result_texts.append(restart_btn)

    # Add back to menu button
    menu_btn = wx.Button(panel, label="Back to Menu", size=(120, 40), pos=(640, 450))
    def _menu_click(e):
        try:
            play_click_sound()
        except Exception:
            pass
        back_to_menu(e)
    menu_btn.Bind(wx.EVT_BUTTON, _menu_click)
    result_texts.append(menu_btn)
    write_game_result(s,x,player1,player2)

    stone.Enable(False)
    paper.Enable(False)
    scissors.Enable(False)
    Rand.Enable(False)


def back_to_menu(event):
    """Return to the main menu"""
    global s, x, round_count, player1_choice, player2_choice, waiting_for_player2
    s = 0
    x = 0
    round_count = 0
    player1_choice = None
    player2_choice = None
    waiting_for_player2 = False
    clear_result_texts()

    # Hide game buttons
    stone.Hide()
    paper.Hide()
    scissors.Hide()
    Rand.Hide()

    mode_text = TransparentText(panel, label="Choose Game Mode", pos=(520, 230))
    medium_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    mode_text.SetFont(medium_font)
    mode_text.SetForegroundColour(wx.Colour(7, 148, 158))
    result_texts.append(mode_text)

    # Show mode selection buttons
    pvp.Show()
    bot_btn.Show()


def restart_game(event):
    global s, x, round_count, player1_choice, player2_choice, waiting_for_player2
    s = 0
    x = 0
    round_count = 0
    player1_choice = None
    player2_choice = None
    waiting_for_player2 = False
    clear_result_texts()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)


def stonein(event):
    play_round("Rock")


def paperin(event):
    play_round("Paper")


def scissorsin(event):
    play_round("Scissors")


def play_round(user_choice):
    global s, x, round_count, player1_choice, player2_choice, waiting_for_player2

    if round_count >= max_rounds:
        return

    # Two-player mode logic
    if is_two_player:
        if not waiting_for_player2:
            # Player 1's turn
            player1_choice = user_choice
            waiting_for_player2 = True
            clear_result_texts()
            stone.Enable(False)
            paper.Enable(False)
            scissors.Enable(False)
            Rand.Enable(False)

            small_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            waiting_text = TransparentText(panel, label=f"{player1} chose! Now {player2}'s turn...", pos=(520, 350))
            waiting_text.SetFont(small_font)
            waiting_text.SetForegroundColour(wx.Colour(171, 1, 255))
            result_texts.append(waiting_text)
            stone.Enable(True)
            paper.Enable(True)
            scissors.Enable(True)
            Rand.Enable(True)
            return
        else:
            # Player 2's turn
            player2_choice = user_choice
            waiting_for_player2 = False
            round_count += 1

            # Now process the round with both choices
            process_round(player1_choice, player2_choice)
    else:
        # Bot mode (original logic)
        round_count += 1
        botchoice()
        choices = ["Rock", "Paper", "Scissors"]
        bot_choice = choices[botchoicein]
        process_round(user_choice, bot_choice)


def process_round(choice1, choice2):
    global s, x

    clear_result_texts()

    small_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    round_text = TransparentText(panel, label=f"Round {round_count}/{max_rounds}", pos=(580, 150))
    round_text.SetFont(small_font)
    result_texts.append(round_text)
    round_text.SetForegroundColour(wx.Colour(7, 148, 158))

    # Show animated hand signs for both players simultaneously at bottom
    show_animated_choices_parallel(choice1, choice2)
    
    # Wait a bit before showing detailed results
    wx.MilliSleep(300)

    text2 = TransparentText(panel, label=f"{player1}'s choice: {choice1}", pos=(400, 350))
    text3 = TransparentText(panel, label=f"{player2}'s choice: {choice2}", pos=(650, 350))
    text2.SetForegroundColour(wx.Colour(1, 135, 255))
    text3.SetForegroundColour(wx.RED)
    text2.SetFont(small_font)
    text3.SetFont(small_font)
    result_texts.extend([text2, text3])

    # Update stats for player1 choice
    if player1 in ["User", "Player 1"] or True:
        # increment trials for the choice1 (player1's choice)
        try:
            choice_stats[choice1]['trials'] += 1
        except Exception:
            pass

    if choice1 == choice2:
        n = "tie"
        tie1 = TransparentText(panel, label="Match was a Tie!", pos=(550, 380))
        tie2 = TransparentText(panel, label=f"{player1} score: {s}", pos=(400, 410))
        tie3 = TransparentText(panel, label=f"{player2} score: {x}", pos=(650, 410))
        tie2.SetFont(small_font)
        tie3.SetFont(small_font)
        tie2.SetForegroundColour(wx.Colour(1, 135, 255))
        tie3.SetForegroundColour(wx.RED)
        tie1.SetFont(small_font)
        result_texts.extend([tie1, tie2, tie3])
        tie1.SetForegroundColour(wx.Colour(171, 1, 255))

    elif (choice1 == "Rock" and choice2 == "Scissors") or \
            (choice1 == "Paper" and choice2 == "Rock") or \
            (choice1 == "Scissors" and choice2 == "Paper"):
        n = "win"
        s += 1
        # record a win for this choice for stats
        try:
            choice_stats[choice1]['wins'] += 1
        except Exception:
            pass
        win1 = TransparentText(panel, label=f"{player1} won! Score: {s}", pos=(400, 380))
        win2 = TransparentText(panel, label=f"{player2} lost! Score: {x}", pos=(650, 380))

        if not is_two_player:
            win3 = TransparentText(panel, label=f"Bot: You were Lucky this time but not forever!!", pos=(400, 410))
            win3.SetForegroundColour(wx.RED)
            win3.SetFont(small_font)
            result_texts.append(win3)

        win1.SetForegroundColour(wx.Colour(1, 135, 255))
        win2.SetForegroundColour(wx.RED)
        win1.SetFont(small_font)
        win2.SetFont(small_font)
        result_texts.extend([win1, win2])

    else:
        n = "lose"
        x += 1
        lost1 = TransparentText(panel, label=f"{player1} lost! Score: {s}", pos=(425, 380))
        lost2 = TransparentText(panel, label=f"{player2} won! Score: {x}", pos=(650, 380))
        lost1.SetForegroundColour(wx.Colour(1, 135, 255))
        lost2.SetForegroundColour(wx.RED)
        lost1.SetFont(small_font)
        lost2.SetFont(small_font)
        result_texts.extend([lost1, lost2])

    # play simple sounds for result (Windows)
    try:
        if n == 'win':
            winsound.Beep(1000, 180)
        elif n == 'lose':
            winsound.Beep(400, 180)
        else:
            winsound.Beep(700, 140)
    except Exception:
        pass

    func_csv(n,round_count)

    if round_count >= 5:
        wx.CallLater(1500, show_game_over)


# Main panel
app = wx.App()
mainwin = wx.Frame(None, title="Rock Paper Scissors", size=(1920, 1080))
panel = wx.Panel(mainwin)



# Background image
try:
    original_bg = wx.Image("ChatGPT Image Dec 8, 2025, 04_19_09 PM.png", wx.BITMAP_TYPE_PNG)

    def on_paint(event):
        dc = wx.PaintDC(panel)
        panel_width, panel_height = panel.GetSize()
        if panel_width > 0 and panel_height > 0:
            # Stretch image to fit panel exactly
            scaled_img = original_bg.Scale(panel_width, panel_height, wx.IMAGE_QUALITY_HIGH)
            dc.DrawBitmap(wx.Bitmap(scaled_img), 0, 0)

    panel.Bind(wx.EVT_PAINT, on_paint)
except:
    panel.SetBackgroundColour(wx.TransparentColour)



text1 = TransparentText(panel, label="Stone Paper Scissors", pos=(500, 200))
large_font = wx.Font(19, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
text1.SetFont(large_font)
text1.SetForegroundColour(wx.Colour(171, 1, 255))

mode_text = TransparentText(panel, label="Choose Game Mode", pos=(520, 230))
medium_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
mode_text.SetFont(medium_font)
mode_text.SetForegroundColour(wx.Colour(7, 148, 158))
result_texts.append(mode_text)


# Game mode buttons
pvp = wx.Button(panel, label="Player vs Player", size=(120, 40), pos=(500, 270))
bot_btn = wx.Button(panel, label="Player vs Bot", size=(120, 40), pos=(640, 270))
def _pvp_click(event):
    try:
        play_click_sound()
    except Exception:
        pass
    twoplayergame()
def _bot_click(event):
    try:
        play_click_sound()
    except Exception:
        pass
    botgame()

pvp.Bind(wx.EVT_BUTTON, _pvp_click)
bot_btn.Bind(wx.EVT_BUTTON, _bot_click)

# Game buttons (initially hidden) - Hexagon Neon Buttons
stone = HexagonNeonButton(panel, label="Rock", neon_color=wx.Colour(255, 0, 0), pos=(400, 250), size=(100, 100))  # Red neon
paper = HexagonNeonButton(panel, label="Paper", neon_color=wx.Colour(0, 100, 255), pos=(520, 250), size=(100, 100))  # Blue neon
scissors = HexagonNeonButton(panel, label="Scissors", neon_color=wx.Colour(0, 255, 100), pos=(640, 250), size=(100, 100))  # Green neon
Rand = HexagonNeonButton(panel, label="Random", neon_color=wx.Colour(120, 40, 180), pos=(760, 250), size=(100, 100))  # Darker purple neon
# Stats button to show probability graph
stats_btn = wx.Button(panel, label="Stats", size=(80, 30), pos=(880, 280))
def _stats_click(e):
    try:
        play_click_sound()
    except Exception:
        pass
    show_stats_dialog(mainwin, choice_stats)
stats_btn.Bind(wx.EVT_BUTTON, _stats_click)

stone.Bind(wx.EVT_BUTTON, stonein)
paper.Bind(wx.EVT_BUTTON, paperin)
scissors.Bind(wx.EVT_BUTTON, scissorsin)
Rand.Bind(wx.EVT_BUTTON, randomuserchoice)

# Hide game buttons initially
stone.Hide()
paper.Hide()
scissors.Hide()
Rand.Hide()
stats_btn.Hide()

mainwin.Show()
app.MainLoop()