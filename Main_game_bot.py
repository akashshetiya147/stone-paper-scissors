import wx
import random
from CSVFORSTORE import *
import math
from name_input import show_name_input
from stats import show_stats_dialog


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
            # === NEW SOUND FUNCTION CALLED HERE ===
            play_minecraft_click()
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

# Stats tracking: separate stats for each player
player1_stats = {
    'Rock': {'trials': 1, 'wins': 0.33},
    'Paper': {'trials': 1, 'wins': 0.33},
    'Scissors': {'trials': 1, 'wins': 0.33}
}

player2_stats = {
    'Rock': {'trials': 1, 'wins': 0.33},
    'Paper': {'trials': 1, 'wins': 0.33},
    'Scissors': {'trials': 1, 'wins': 0.33}
}


def botgame():
    global player1, player2, is_two_player, player1_stats, player2_stats
    
    # Get player name from dialog
    result = show_name_input(mainwin, is_two_player=False)
    if result is None:  # User cancelled
        return
    
    player1 = result
    player2 = "Bot"
    is_two_player = False
    
    # Reset stats for new game
    player1_stats = {
        'Rock': {'trials': 1, 'wins': 0.33},
        'Paper': {'trials': 1, 'wins': 0.33},
        'Scissors': {'trials': 1, 'wins': 0.33}
    }
    player2_stats = {
        'Rock': {'trials': 1, 'wins': 0.33},
        'Paper': {'trials': 1, 'wins': 0.33},
        'Scissors': {'trials': 1, 'wins': 0.33}
    }
    
    restart_game(None)

    pvp.Hide()
    bot_btn.Hide()
    stone.Show()
    paper.Show()
    scissors.Show()
    Rand.Show()
    stats_btn.Show()
    player1_stats_btn.Hide()
    player2_stats_btn.Hide()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)

    clear_result_texts()


def twoplayergame():
    global player1, player2, is_two_player, player1_stats, player2_stats
    
    # Get player names from dialog
    result = show_name_input(mainwin, is_two_player=True)
    if result is None:  # User cancelled
        return
    player1, player2 = result
    is_two_player = True
    
    # Reset stats for new game
    player1_stats = {
        'Rock': {'trials': 1, 'wins': 0.33},
        'Paper': {'trials': 1, 'wins': 0.33},
        'Scissors': {'trials': 1, 'wins': 0.33}
    }
    player2_stats = {
        'Rock': {'trials': 1, 'wins': 0.33},
        'Paper': {'trials': 1, 'wins': 0.33},
        'Scissors': {'trials': 1, 'wins': 0.33}
    }
    
    # Update button labels
    player1_stats_btn.SetLabel(f"{player1} Stats")
    player2_stats_btn.SetLabel(f"{player2} Stats")
    
    restart_game(None)
    # Hide mode selection buttons
    pvp.Hide()
    bot_btn.Hide()
    # Show and enable game buttons
    stone.Show()
    paper.Show()
    scissors.Show()
    Rand.Show()
    stats_btn.Hide()
    player1_stats_btn.Show()
    player2_stats_btn.Show()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)
    
    stone.Enable(False)
    paper.Enable(False)
    scissors.Enable(False)
    Rand.Enable(False)

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
    def on_restart(e):
        # === NEW SOUND FUNCTION CALLED HERE ===
        play_minecraft_click()
        restart_game(e)
    restart_btn.Bind(wx.EVT_BUTTON, on_restart)
    result_texts.append(restart_btn)

    # Add back to menu button
    menu_btn = wx.Button(panel, label="Back to Menu", size=(120, 40), pos=(640, 450))
    def on_menu(e):
        # === NEW SOUND FUNCTION CALLED HERE ===
        play_minecraft_click()
        back_to_menu(e)
    menu_btn.Bind(wx.EVT_BUTTON, on_menu)
    result_texts.append(menu_btn)
    write_game_result(s,x,player1,player2)

    stone.Enable(False)
    paper.Enable(False)
    scissors.Enable(False)
    Rand.Enable(False)
    stats_btn.Hide()
    player1_stats_btn.Hide()
    player2_stats_btn.Hide()


def back_to_menu(event):
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

    if round_count == max_rounds:
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
    global s, x, player1_stats, player2_stats

    clear_result_texts()

    small_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    round_text = TransparentText(panel, label=f"Round {round_count}/{max_rounds}", pos=(580, 150))
    round_text.SetFont(small_font)
    result_texts.append(round_text)
    round_text.SetForegroundColour(wx.Colour(7, 148, 158))

    text2 = TransparentText(panel, label=f"{player1}'s choice: {choice1}", pos=(400, 350))
    text3 = TransparentText(panel, label=f"{player2}'s choice: {choice2}", pos=(650, 350))
    text2.SetForegroundColour(wx.Colour(1, 135, 255))
    text3.SetForegroundColour(wx.RED)
    text2.SetFont(small_font)
    text3.SetFont(small_font)
    result_texts.extend([text2, text3])

    # Update stats for both players
    player1_stats[choice1]['trials'] += 1
    player2_stats[choice2]['trials'] += 1

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
        player1_stats[choice1]['wins'] += 1
        
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
        # Player2 wins - increment their wins for this choice
        player2_stats[choice2]['wins'] += 1
        
        lost1 = TransparentText(panel, label=f"{player1} lost! Score: {s}", pos=(425, 380))
        lost2 = TransparentText(panel, label=f"{player2} won! Score: {x}", pos=(650, 380))
        lost1.SetForegroundColour(wx.Colour(1, 135, 255))
        lost2.SetForegroundColour(wx.RED)
        lost1.SetFont(small_font)
        lost2.SetFont(small_font)
        result_texts.extend([lost1, lost2])

    func_csv(n, round_count)

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

pvp = wx.Button(panel, label="Player vs Player", size=(120, 40), pos=(500, 270))
bot_btn = wx.Button(panel, label="Player vs Bot", size=(120, 40), pos=(640, 270))



stone = HexagonNeonButton(panel, label="Rock", neon_color=wx.Colour(255, 0, 0), pos=(400, 250), size=(100, 100))
paper = HexagonNeonButton(panel, label="Paper", neon_color=wx.Colour(0, 100, 255), pos=(520, 250), size=(100, 100))
scissors = HexagonNeonButton(panel, label="Scissors", neon_color=wx.Colour(0, 255, 100), pos=(640, 250), size=(100, 100))
Rand = HexagonNeonButton(panel, label="Random", neon_color=wx.Colour(120, 40, 180), pos=(760, 250), size=(100, 100))

# Stats button to show probability graph
stats_btn = wx.Button(panel, label="Stats", size=(80, 30), pos=(880, 280))

# Create two separate stats buttons for two-player mode
player1_stats_btn = wx.Button(panel, label=f"{player1} Stats", size=(100, 30), pos=(850, 250))
player2_stats_btn = wx.Button(panel, label=f"{player2} Stats", size=(100, 30), pos=(850, 290))

def on_stats_click(e):
    show_stats_dialog(mainwin, player1_stats, player1)

def on_player1_stats_click(e):
    show_stats_dialog(mainwin, player1_stats, player1)

def on_player2_stats_click(e):
    show_stats_dialog(mainwin, player2_stats, player2)

stats_btn.Bind(wx.EVT_BUTTON, on_stats_click)
player1_stats_btn.Bind(wx.EVT_BUTTON, on_player1_stats_click)
player2_stats_btn.Bind(wx.EVT_BUTTON, on_player2_stats_click)

stone.Bind(wx.EVT_BUTTON, stonein)
paper.Bind(wx.EVT_BUTTON, paperin)
scissors.Bind(wx.EVT_BUTTON, scissorsin)
Rand.Bind(wx.EVT_BUTTON, randomuserchoice)

stone.Hide()
paper.Hide()
scissors.Hide()
Rand.Hide()
stats_btn.Hide()
player1_stats_btn.Hide()
player2_stats_btn.Hide()

mainwin.Show()
app.MainLoop()