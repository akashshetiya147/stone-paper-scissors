import wx
import random

# --- Transparent Text Class ---I dont know how this works but its cool
#i did not do this but stack overflow did this it was very usefull
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



# --- GAME LOGIC ---
s = 0
x = 0
ranusch=0
botchoicein = 0
round_count = 0
max_rounds = 5
result_texts = []


def botchoice():
    global botchoicein
    botchoicein = random.randint(0, 2)
def randomuserchoice(event):
    global ranusch
    ranusch = random.randint(0, 2)
    choice= ["Scissors","Rock", "Paper"]
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

    game_over_text = TransparentText(panel, label="GAME OVER!", pos=(550, 300))
    game_over_text.SetFont(large_font)
    game_over_text.SetForegroundColour(wx.Colour(255, 0, 0))
    result_texts.append(game_over_text)

    if s > x:
        winner_text = TransparentText(panel, label=f"YOU  WIN!  Final Score - You: {s}, Bot: {x}", pos=(435, 350))
        winner_text.SetForegroundColour(wx.Colour(1,135,255))
    elif x > s:
        winner_text = TransparentText(panel, label=f"BOT  WINS! Final Score - You: {s}, Bot: {x}", pos=(435, 350))
        winner_text.SetForegroundColour(wx.RED)
    else:
        winner_text = TransparentText(panel, label=f"IT'S A TIE! Final Score - You: {s}, Bot: {x}", pos=(435, 350))
        winner_text.SetForegroundColour(wx.Colour(171,1,255))

    winner_text.SetFont(medium_font)
    result_texts.append(winner_text)

    restart_btn = wx.Button(panel, label="Restart Game", size=(120, 40), pos=(575, 400))
    restart_btn.Bind(wx.EVT_BUTTON, restart_game)
    result_texts.append(restart_btn)

    stone.Enable(False)
    paper.Enable(False)
    scissors.Enable(False)


def restart_game(event):
    global s, x, round_count
    s = 0
    x = 0
    round_count = 0
    clear_result_texts()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)


def stonein(event):
    play_round("Rock")


def paperin(event):
    play_round("Paper")


def scissorsin(event):
    play_round("Scissors")


def play_round(user):
    global s, x, round_count

    if round_count >= max_rounds:
        return

    round_count += 1
    clear_result_texts()

    botchoice()
    small_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    choices = ["Rock", "Paper", "Scissors"]
    bot = choices[botchoicein]

    round_text = TransparentText(panel, label=f"Round {round_count}/{max_rounds}", pos=(580, 150))
    round_text.SetFont(small_font)
    result_texts.append(round_text)
    round_text.SetForegroundColour(wx.Colour(7,148,158))

    text2 = TransparentText(panel, label=f"Your choice: {user}", pos=(450, 300))
    text3 = TransparentText(panel, label=f"Bot choice: {bot}", pos=(650, 300))
    text2.SetForegroundColour(wx.Colour(1,135,255))
    text3.SetForegroundColour(wx.RED)
    text2.SetFont(small_font)
    text3.SetFont(small_font)
    result_texts.extend([text2, text3])

    if user == bot:
        tie1 = TransparentText(panel, label="Match was a tie!", pos=(550, 330))
        tie1.SetFont(small_font)
        result_texts.append(tie1)
        tie1.SetForegroundColour(wx.Colour(171,1,255))

    elif (user == "Rock" and bot == "Scissors") or \
         (user == "Paper" and bot == "Rock") or \
         (user == "Scissors" and bot == "Paper"):
        s += 1
        win1 = TransparentText(panel, label=f"You won! Your score: {s}", pos=(425, 330))
        win2 = TransparentText(panel, label=f"Bot score: {x}", pos=(650, 330))
        win3=TransparentText(panel, label=f"Bot:You were Lucky this time but not forever!!",pos=(450, 360))
        win3.SetForegroundColour(wx.RED)
        win3.SetFont(small_font)
        win1.SetForegroundColour(wx.Colour(1,135,255))
        win2.SetForegroundColour(wx.RED)
        win1.SetFont(small_font)
        win2.SetFont(small_font)
        result_texts.extend([win1, win2,win3])

    else:
        x += 1
        lost1 = TransparentText(panel, label=f"You lost! Your score: {s}", pos=(425, 330))
        lost2 = TransparentText(panel, label=f"Bot won! Bot score: {x}", pos=(650, 330))
        lost1.SetForegroundColour(wx.Colour(1,135,255))
        lost2.SetForegroundColour(wx.RED)
        lost1.SetFont(small_font)
        lost2.SetFont(small_font)
        result_texts.extend([lost1, lost2])

    if round_count >= 5:
        wx.CallLater(1500, show_game_over)


app = wx.App()
mainwin = wx.Frame(None, title="Rock Paper Scissors", size=(1920, 100))
panel = wx.Panel(mainwin)

#using stack overflow for putting a bg image
try:
    bg = wx.Bitmap("./2951232.jpeg")

    def on_paint(event):
        dc = wx.PaintDC(panel)
        dc.DrawBitmap(bg, 0, 0)

    panel.Bind(wx.EVT_PAINT, on_paint)
except:
    panel.SetBackgroundColour(wx.TransparentColour)



text1 = TransparentText(panel, label="Stone Paper Scissors", pos=(500, 200))
large_font = wx.Font(19, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
text1.SetFont(large_font)
text1.SetForegroundColour(wx.Colour(171,1,255))

stone = wx.Button(panel, label="Rock", size=(60, 30), pos=(480, 260))
paper = wx.Button(panel, label="Paper", size=(60, 30), pos=(560, 260))
scissors = wx.Button(panel, label="Scissors", size=(60, 30), pos=(640, 260))
Rand=wx.Button(panel, label="Random", size=(60, 30), pos=(720, 260))

stone.Bind(wx.EVT_BUTTON, stonein)
paper.Bind(wx.EVT_BUTTON, paperin)
scissors.Bind(wx.EVT_BUTTON, scissorsin)
Rand.Bind(wx.EVT_BUTTON,randomuserchoice)


mainwin.Show()
app.MainLoop()