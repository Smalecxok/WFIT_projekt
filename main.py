import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad
import pygame
import math

wartoscDlugosci = ""
wartoscKata=""
g=9.81
uproszczony=0.0
faktyczny=0.0

def integrand(kk, k):
    return 1/(np.sqrt(np.cos(kk)-np.cos(k)))

def sprawdzaj1():

    if len(text1.get("1.0", "end"))==1:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")
        return 1

def sprawdzaj2():

    if len(text2.get("1.0", "end")) == 1:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")

        return 1



def licz():

    wartoscDlugosci = text1.get("1.0","end")
    wartoscKata = text2.get("1.0","end")


    try:

        l = float(wartoscDlugosci)
        k = float(wartoscKata)

    except:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")

        return

    uproszczony = 2 * np.pi * np.sqrt(l / g)

    roundOff = np.round_(uproszczony * 10000) / 10000

    text3.delete(1.0, "end")
    text3.insert(1.0, roundOff)


    radians = np.radians(k);

    faktyczny = quad(integrand, 0, radians, args=(radians))



    roundOff2 = np.round(faktyczny[0] *  4 * np.sqrt(l/(2*g))*10000) / 10000;
    text4.delete(1.0, "end")
    text4.insert(1.0,roundOff2)

def rysuj():

    if sprawdzaj1() == 1:
        return




    wartoscDlugosci = text1.get("1.0", "end")


    try:

        l = float(wartoscDlugosci)

    except:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")

        return


    l = float(wartoscDlugosci)

    dev_x = []
    dev_y1 = []
    dev_y2 = []

    for x in range(90):
        dev_x.append(x)
        uproszczony=2 * np.pi * np.sqrt(l / g)
        dev_y1.append(uproszczony)
        radians = np.radians(x)

        faktyczny = quad(integrand, 0, radians, args=(radians))

        dev_y2.append(faktyczny[0]* 4 * np.sqrt(l/(2*g)))

    plt.plot(dev_x,dev_y1,  label="Prosty wzrór")
    plt.plot(dev_x, dev_y2,   label="Dokładny wzór całkowy")

    plt.xlabel('Wychylenie w stopniach')
    plt.ylabel('Okres wahadła')

    plt.title('Dla długości wahadła = ' + wartoscDlugosci)

    plt.legend()
    plt.show()


def animacja():

    speed=100
    mode = 0
    mode2=0
    run = True
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    q1 = text2.get("1.0","end")
    swing=np.radians(float(q1))

    q2 = text3.get("1.0","end")
    period = float(q2)

    q3 = text4.get("1.0", "end")
    period2 = float(q3)

    angle=np.pi/2
    angle2=np.pi/2
    print(swing)
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    screen.fill(white)

    while run:
        msElapsed = clock.tick(4*speed / period)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill(white)

        pygame.draw.circle(screen, black, (int(math.cos(angle) * 100) + 300, int(math.sin(angle) * 100) + 300), 10)

        pygame.draw.line(screen, black, (300,300), (int(math.cos(angle) * 100) + 300, int(math.sin(angle) * 100) + 300), 5)

        pygame.draw.circle(screen, (255,0,0), (int(math.cos(angle2) * 100) + 300, int(math.sin(angle2) * 100) + 300), 10)

        pygame.draw.line(screen, red, (300, 300), (int(math.cos(angle2) * 100) + 300, int(math.sin(angle2) * 100) + 300), 5)

        pygame.draw.line(screen, black, (100, 300), (500, 300), 5)


        pygame.display.flip()



        if mode == 0:
            angle = angle + swing/(period*speed)
        else:
            angle = angle - swing/(period*speed)

        if mode2 == 0:
            angle2 = angle2 + swing / (period2 * speed)
        else:
            angle2 = angle2 - swing / (period2 * speed)


        if angle > np.pi / 2 + swing:
            mode = 1
        if angle < np.pi / 2 - swing:
             mode = 0


        if angle2 > np.pi / 2 + swing:
            mode2 = 1
        if angle2 < np.pi / 2 - swing:
             mode2 = 0

        print(angle)

    pygame.quit()




#interfejs graficzny

root = tk.Tk()
root.title('Zależność okresu wahadła od wychylenia')

canvas = tk.Canvas(root, height = 700, width = 700, bg="#263D42")
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

label1 = tk.Label(root, height=3, bg="#263D42",fg="white", text = "Podaj długość [m]")
label1.place(x = 10, y = 100)

label2 = tk.Label(root, height=3, bg="#263D42",fg="white", text = "Podaj kąt [°]")
label2.place(x = 10, y = 200)

label3 = tk.Label(root, height=3, bg="#263D42",fg="white", text = "wynik uproszczony [s]")
label3.place(x = 370, y = 100)

label4 = tk.Label(root, height=3, bg="#263D42",fg="white", text = "wynik faktyczny [s]")
label4.place(x = 370, y = 200)

wpisz= tk.Button(root, text="Pokaż wynik", padx = 10, pady = 10, fg="white", bg="#263D42", width=10, height= 3, command=licz)
wpisz.place(x = 100, y= 400)

generuj= tk.Button(root, text="Rysuj wykers zależności okresu od kąta", padx = 10, pady = 10, fg="white", bg="#263D42", width=30, height= 3, command=rysuj)
generuj.place(x = 400, y= 400)

animacja= tk.Button(root, text="Animacja", padx = 10, pady = 10, fg="white", bg="#263D42", width=30, height= 3, command=animacja)
animacja.place(x = 300, y= 600)


root.resizable(False, False)

root.mainloop()


