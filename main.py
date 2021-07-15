import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad
import pygame
import math

wartoscDlugosci = ""
wartoscKata=""
uproszczony=0.0
faktyczny=0.0

G=9.81

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 128)
TURQUOISE = '#263d42'

START_MESSAGE = "Podaj długość i kąt"
NOT_ENOUGH_MESSAGE = "Niewystarczająca ilość danych"

def integrand(kk, k):
    return 1/(np.sqrt(np.cos(kk)-np.cos(k)))

def reset():
    pass

def showMessage(message):

    var.set(message)
    message_label.pack()

def licz():

    wartoscDlugosci = text1.get("1.0","end")
    wartoscKata = text2.get("1.0","end")

    try:

        l = float(wartoscDlugosci)
        k = float(wartoscKata)

    except:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")
        showMessage(NOT_ENOUGH_MESSAGE)

        return

    showMessage(START_MESSAGE)

    uproszczony = 2 * np.pi * np.sqrt(l / G)
    roundOff = np.round_(uproszczony * 1000000000) / 1000000000
    text3.delete(1.0, "end")
    text3.insert(1.0, roundOff)

    radians = np.radians(k);

    faktyczny = quad(integrand, 0, radians, args=(radians))
    roundOff2 = np.round(faktyczny[0] * 4 * np.sqrt(l / (2 * G)) * 1000000000) / 1000000000;
    text4.delete(1.0, "end")
    text4.insert(1.0,roundOff2)

def rysuj():

    wartoscDlugosci = text1.get("1.0", "end")

    try:

        l = float(wartoscDlugosci)

    except:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")
        showMessage(NOT_ENOUGH_MESSAGE)
        return

    showMessage(START_MESSAGE)

    dev_x = []
    dev_y1 = []
    dev_y2 = []

    for x in range(90):
        dev_x.append(x+1)
        uproszczony= 2 * np.pi * np.sqrt(l / G)
        dev_y1.append(uproszczony)
        radians = np.radians(x+1)

        faktyczny = quad(integrand, 0, radians, args=(radians))

        dev_y2.append(faktyczny[0] * 4 * np.sqrt(l / (2 * G)))

    plt.plot(dev_x,dev_y1,  label="Prosty wzrór")
    plt.plot(dev_x, dev_y2,   label="Dokładny wzór całkowy")

    plt.xlabel('Wychylenie w stopniach')
    plt.ylabel('Okres wahadła')

    plt.title('Dla długości wahadła = ' + wartoscDlugosci)

    plt.legend()
    plt.show()


def animacja():

    wartoscDlugosci = text1.get("1.0", "end")
    wartoscKata = text2.get("1.0", "end")
    obliczona1 = text3.get("1.0", "end")
    obliczona2 = text4.get("1.0", "end")

    try:

        float(wartoscDlugosci)
        float(wartoscKata)
        float(obliczona1)
        float(obliczona2)

    except:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")
        showMessage("Najpierw wciśnij przycisk oblicz")
        return

    showMessage(START_MESSAGE)

    pygame.init()
    pygame.display.set_caption('Animacja')

    X_SHIFT=400
    Y_SHIFT=100

    SPEED=60
    mode = 0
    mode2=0
    run = True


    q1 = text2.get("1.0","end")
    swing=np.radians(float(q1))

    q2 = text3.get("1.0","end")
    period = float(q2)

    q3 = text4.get("1.0", "end")
    period2 = float(q3)

    angle=np.pi/2-swing
    angle2=np.pi/2-swing

    SIZE = WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode(SIZE)


    screen.fill(WHITE)

    FONT = pygame.font.Font('freesansbold.ttf', 20)

    mode_changes = 0
    mode_changes2 = 0
    clock = pygame.time.Clock()

    while run:

        clock.tick_busy_loop(4*SPEED)

        time = int(pygame.time.get_ticks())

        tekst_info = "okresy czarnego wahadła: " + str(mode_changes)
        tekst_info2 = "okresy czerwonego wahadła: " + str(mode_changes2)
        time_info = "czas: " + str(time) + " ms"

        tekst = FONT.render(tekst_info, True, WHITE, TURQUOISE)
        tekstRect = tekst.get_rect()
        tekstRect.center = (200, 20)

        tekst2 = FONT.render(tekst_info2, True, WHITE, TURQUOISE)
        tekstRect2 = tekst2.get_rect()
        tekstRect2.center = (600, 20)

        tekst3 = FONT.render(time_info, True, WHITE, TURQUOISE)
        tekstRect3 = tekst3.get_rect()
        tekstRect3.center = (400, 250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(TURQUOISE)
        screen.blit(tekst, tekstRect)
        screen.blit(tekst2, tekstRect2)
        screen.blit(tekst3, tekstRect3)

        #pygame.display.update()

        pygame.draw.circle(screen, BLACK, (int(math.cos(angle) * 100) + X_SHIFT, int(math.sin(angle) * 100) + Y_SHIFT), 10)

        pygame.draw.line(screen, BLACK, (X_SHIFT,Y_SHIFT), (int(math.cos(angle) * 100) + X_SHIFT, int(math.sin(angle) * 100) + Y_SHIFT), 5)

        pygame.draw.circle(screen, RED, (int(math.cos(angle2) * 100) + X_SHIFT, int(math.sin(angle2) * 100) + Y_SHIFT), 10)

        pygame.draw.line(screen, RED, (X_SHIFT, Y_SHIFT), (int(math.cos(angle2) * 100) + X_SHIFT, int(math.sin(angle2) * 100) + Y_SHIFT), 5)

        pygame.draw.line(screen, BLACK, (300, Y_SHIFT), (500, Y_SHIFT), 5)

        pygame.display.flip()

        if mode == 0:
            angle = angle + (swing/(period*SPEED))

        else:
            angle = angle - swing/(period*SPEED)

        if mode2 == 0:
            angle2 = angle2 + swing / (period2 *SPEED)
        else:
            angle2 = angle2 - swing / (period2 *SPEED)

        previous_mode= mode
        previous_mode2 = mode2

        if angle > np.pi / 2 + swing:
            mode = 1
        if angle < np.pi / 2 - swing:
             mode = 0

        if mode != previous_mode and mode ==0:
            mode_changes=mode_changes+1

        if angle2 > np.pi / 2 + swing:
            mode2 = 1
        if angle2 < np.pi / 2 - swing:
             mode2 = 0

        if mode2 != previous_mode2 and mode2 ==0:
            mode_changes2=mode_changes2+1

    pygame.quit()

#interfejs graficzny

buttons_height=300
message = START_MESSAGE

root = tk.Tk()
root.title('Zależność okresu wahadła od wychylenia')

canvas = tk.Canvas(root, height = 400, width = 700, bg=TURQUOISE)
canvas.pack()

frame = tk.Frame(root, bg = "white")

text1 = tk.Text(root, width=20,height=3,)
text1.place(x = 150, y= 100)

text2 = tk.Text(root, width=20,height=3)
text2.place(x = 150, y= 200)

text3 = tk.Text(root, width=20,height=3)
text3.place(x = 500, y= 100)

text4 = tk.Text(root, width=20,height=3)
text4.place(x = 500, y= 200)

label1 = tk.Label(root, height=3, bg=TURQUOISE, fg="white", text ="Podaj długość [m]")
label1.place(x = 10, y = 100)

label2 = tk.Label(root, height=3, bg=TURQUOISE, fg="white", text ="Podaj kąt [°]")
label2.place(x = 10, y = 200)

label3 = tk.Label(root, height=3, bg=TURQUOISE, fg="white", text ="wynik uproszczony [s]")
label3.place(x = 370, y = 100)

label4 = tk.Label(root, height=3, bg=TURQUOISE, fg="white", text ="wynik faktyczny [s]")
label4.place(x = 370, y = 200)

pokaz_wynik= tk.Button(root, text="Pokaż wynik", padx = 10, pady = 10, fg="white", bg=TURQUOISE, width=10, height= 3, command=licz)
pokaz_wynik.place(x = 40, y= buttons_height)

rysuj_wykres= tk.Button(root, text="Rysuj wykers zależności okresu od kąta", padx = 10, pady = 10, fg="white", bg=TURQUOISE, width=30, height= 3, command=rysuj)
rysuj_wykres.place(x = 140, y= buttons_height)

animacja= tk.Button(root, text="Animacja", padx = 10, pady = 10, fg="white", bg=TURQUOISE, width=30, height= 3, command=animacja)
animacja.place(x = 380, y= buttons_height)

var = tk.StringVar()
message_label = tk.Label( root, textvariable=var, relief = tk.RAISED )

var.set(message)

message_label.pack()

root.resizable(False, False)

root.mainloop()


