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

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
turquoise = '#263d42'

start_message = "Podaj długość i kąt"


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
        showMessage("Niewystarczająca ilość danych")

        return

    showMessage(start_message)

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

    # if sprawdzaj1() == 1:
    #     return


    wartoscDlugosci = text1.get("1.0", "end")


    try:

        l = float(wartoscDlugosci)

    except:

        text3.delete(1.0, "end")
        text4.delete(1.0, "end")
        showMessage("Niewystarczająca ilość danych")
        return

    showMessage(start_message)

    dev_x = []
    dev_y1 = []
    dev_y2 = []

    for x in range(90):
        dev_x.append(x+1)
        uproszczony= 2 * np.pi * np.sqrt(l / g)
        dev_y1.append(uproszczony)
        radians = np.radians(x+1)

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

    showMessage(start_message)

    pygame.init()
    pygame.display.set_caption('Animacja')

    x_shift=400
    y_shift=100

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
    # print(swing)
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    screen.fill(white)

    font = pygame.font.Font('freesansbold.ttf', 20)

    while run:
        clock.tick(speed*4)



        # print(str(pygame.time.get_ticks()))

        time = int(pygame.time.get_ticks())

        tekst_info = "okresy czarnego wahadła: " + str(int(time/(1000*period)))
        tekst_info2= "okresy czerwonego wahadła: " + str(int(time/(1000*period2)))
        time_info = "czas: " + str(time) + " ms"

        tekst = font.render(tekst_info, True, white, turquoise)
        tekstRect = tekst.get_rect()
        tekstRect.center = (200, 20)

        tekst2 = font.render(tekst_info2, True, white, turquoise)
        tekstRect2 = tekst2.get_rect()
        tekstRect2.center = (600, 20)

        tekst3 = font.render(time_info, True, white, turquoise)
        tekstRect3 = tekst3.get_rect()
        tekstRect3.center = (400, 250)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(turquoise)
        screen.blit(tekst, tekstRect)
        screen.blit(tekst2, tekstRect2)
        screen.blit(tekst3, tekstRect3)

        # pygame.display.update()

        pygame.draw.circle(screen, black, (int(math.cos(angle) * 100) + x_shift, int(math.sin(angle) * 100) + y_shift), 10)

        pygame.draw.line(screen, black, (x_shift,y_shift), (int(math.cos(angle) * 100) + x_shift, int(math.sin(angle) * 100) + y_shift), 5)

        pygame.draw.circle(screen, red, (int(math.cos(angle2) * 100) + x_shift, int(math.sin(angle2) * 100) + y_shift), 10)

        pygame.draw.line(screen, red, (x_shift, y_shift), (int(math.cos(angle2) * 100) + x_shift, int(math.sin(angle2) * 100) + y_shift), 5)


        pygame.draw.line(screen, black, (300, y_shift), (500, y_shift), 5)


        pygame.display.flip()



        if mode == 0:
            angle = angle + swing/(period*speed)
        else:
            angle = angle - swing/(period*speed)

        if mode2 == 0:
            angle2 = angle2 + swing / (period2 *speed)
        else:
            angle2 = angle2 - swing / (period2 *speed)


        if angle > np.pi / 2 + swing:
            mode = 1
        if angle < np.pi / 2 - swing:
             mode = 0


        if angle2 > np.pi / 2 + swing:
            mode2 = 1
        if angle2 < np.pi / 2 - swing:
             mode2 = 0



    pygame.quit()




#interfejs graficzny

buttons_height=300
message = start_message

root = tk.Tk()
root.title('Zależność okresu wahadła od wychylenia')

canvas = tk.Canvas(root, height = 400, width = 700, bg=turquoise)
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

label1 = tk.Label(root, height=3, bg=turquoise,fg="white", text = "Podaj długość [m]")
label1.place(x = 10, y = 100)

label2 = tk.Label(root, height=3, bg=turquoise,fg="white", text = "Podaj kąt [°]")
label2.place(x = 10, y = 200)

label3 = tk.Label(root, height=3, bg=turquoise,fg="white", text = "wynik uproszczony [s]")
label3.place(x = 370, y = 100)

label4 = tk.Label(root, height=3, bg=turquoise,fg="white", text = "wynik faktyczny [s]")
label4.place(x = 370, y = 200)

pokaz_wynik= tk.Button(root, text="Pokaż wynik", padx = 10, pady = 10, fg="white", bg=turquoise, width=10, height= 3, command=licz)
pokaz_wynik.place(x = 40, y= buttons_height)

rysuj_wykres= tk.Button(root, text="Rysuj wykers zależności okresu od kąta", padx = 10, pady = 10, fg="white", bg=turquoise, width=30, height= 3, command=rysuj)
rysuj_wykres.place(x = 140, y= buttons_height)

animacja= tk.Button(root, text="Animacja", padx = 10, pady = 10, fg="white", bg=turquoise, width=30, height= 3, command=animacja)
animacja.place(x = 380, y= buttons_height)

var = tk.StringVar()
message_label = tk.Label( root, textvariable=var, relief = tk.RAISED )

var.set(message)

message_label.pack()


root.resizable(False, False)

root.mainloop()


