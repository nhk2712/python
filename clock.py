from tkinter import *
from tkinter import ttk
from datetime import datetime
import pyglet
from tkinter import messagebox

pyglet.font.add_file('fonts/pixelinvert.ttf')
pyglet.font.add_file('fonts/pixel.ttf')
pyglet.font.add_file('fonts/7segment.ttf')  # Untitled1
pyglet.font.add_file('fonts/7segmentbit.ttf')  # 7segment

app = Tk()
app.title('Clock')
app.configure(background='white')
app.iconbitmap("sq.ico")
app.resizable(False,False)

control = Frame(app, padx=100, pady=40, bg="#ffffff")
control.pack()

options = [
    "Default",
    "7-segment",
    "Rectangle",
    "Light",
    "7-segment pixel",
    "Rectangle (inverted)"
]

fontStyles = [
    ("Calibri", 200),
    ("untitled1", 150),
    ("pixel", 230),
    ("Calibri light", 210),
    ("7segment", 250),
    ("pixelinvert", 200)
]

vari = StringVar(app)
vari.set(options[0])

fontStart = "Default"


def change():
    global fontStart
    fontStart = font.get()


fontOptn = Frame(control, pady=10, bg="#ffffff")
fontOptn.pack()
font = ttk.Combobox(fontOptn, textvariable=vari,
                    postcommand=change, values=options)
font.pack()

clock = None


def quit(e):
    app.quit()


def loop():
    global clock
    now = datetime.now()
    curTime = now.strftime("%H:%M:%S")
    clock.configure(text=curTime)
    app.after(1000, loop)


def getIndex():
    global options
    num = -1
    for i in range(len(options)):
        if options[i] == vari.get():
            num = i
            return num


def funStart():
    global clock, fontStyles
    try:
        style = fontStyles[getIndex()]
    except TypeError:
        messagebox.showerror("Error", "Invalid option.")
        return
    app.attributes('-fullscreen', True)
    app.configure(background='black', cursor='none')
    app.bind('<Button-1>', quit)
    app.bind('<Key>', quit)

    control.destroy()

    now = datetime.now()
    curTime = now.strftime("%H:%M:%S")

    clock = Label(app, text=curTime, bg='black', fg="#dddddd", font=style)
    clock.place(relx='0.5', rely='0.5', anchor='center')

    app.after(1000, loop)


startBtn = Frame(control, pady=10, bg="#ffffff")
startBtn.pack()
start = Button(startBtn, text="Start", bg="#00dd00", fg="#ffffff", relief="flat", font=(
    "Segoe UI", 15), padx=15, activebackground="#00aa00", activeforeground="#ffffff", cursor="hand2", command=funStart)
start.pack()

app.mainloop()
