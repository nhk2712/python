from tkinter import *

app = Tk()
app.title("tmp.txt - SuperNote")

f=open("tmp.txt","r+")
a=f.read()

txt = Text(app)
txt.config(font=("Times New Roman",14))
txt.insert("1.0",a)
txt.pack()

def edit(e):
    f.seek(0)
    f.truncate(0)
    a=txt.get("1.0","end")
    f.write(a)

txt.bind('<KeyRelease>',edit)

app.mainloop()