from tkinter import *
from datetime import datetime

now=datetime.now()
curTime=now.strftime("%H:%M:%S")

app = Tk()
app.title('Clock')
app.attributes('-fullscreen',True)
app.configure(background='black',cursor='none')

clock = Label(app,text=curTime,bg='black',fg="#dddddd",font=("Calibri", 200))
clock.place(relx='0.5',rely='0.5',anchor='center')

def quit(e):
    app.quit()
app.bind('<Button-1>',quit)

def loop():
    global clock
    now=datetime.now()
    curTime=now.strftime("%H:%M:%S")
    clock.configure(text=curTime)
    app.after(1000,loop)
app.after(1000,loop)
app.mainloop()