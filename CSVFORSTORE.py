import csv
import os

p2r = ""
p1r = ""
c=0

def func_csv(n, round_count):
    global p2r, p1r
    if n == "win":
        p1r += (str(round_count) + ",")
        p2r += ""
    elif n == "lose":
        p1r += ""
        p2r += (str(round_count) + ",")
    else:
        p1r += ""
        p2r += ""


def write_game_result(s, x,player1,player2):

    global p2r, p1r,c
    c+=1
    file_exists = os.path.isfile("User.csv")

    with open("User.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Player", "Final Score", "Winning Rounds"])

        writer.writerow([f"Rock Paper Scissors - Game Results{c}"])
        writer.writerow([player1, s, p1r])
        writer.writerow([player2, x, p2r])
        writer.writerow([])
    p1r=""
    p2r=""



