from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename,asksaveasfile
from tkinter import messagebox
import numpy as np
import math

# App info
app = Tk()
app.title('Image Editor')
app.geometry('640x480')
app.state('zoomed')
app.iconbitmap('icon.ico')

# Global variables
rootImg = None
img = None
act = False

alpha=1
beta=0
gamma=1
blurLvl = 1
gauBlurLvl = 1
medBlurLvl = 1

# UI components
control = Label(app)
control.pack(side=RIGHT)

placeholder = Image.open('placeholder.png')
placeholder = ImageTk.PhotoImage(placeholder)

imgDisp = Label(app, image=placeholder)
imgDisp.image = placeholder
imgDisp.place(relx=0.5,rely=0.5,anchor=CENTER)

ctrlTitle = Label(control, text="Control zone")
ctrlTitle.pack(side=TOP)

def editImg():
    global alpha,beta,gamma
    global rootImg,img,act
    global blurLvl,gauBlurLvl,medBlurLvl
    act=True

    img = cv.convertScaleAbs(rootImg, alpha=alpha, beta=beta)
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    img = cv.LUT(img, lookUpTable)

    img = cv.blur(img,(blurLvl,blurLvl))
    img = cv.GaussianBlur(img,(gauBlurLvl,gauBlurLvl),0)
    img=cv.medianBlur(img,medBlurLvl)

    renderImg()

#
# Control zone UI
#

brightTitle = Label(control, text="Brightness")
contrastTitle = Label(control, text="Contrast")
gamCorrectTitle = Label(control,text="Gamma correction")
blurTitle = Label(control,text='Blur')
gausTitle = Label(control,text='Gaussian blur')
medTitle = Label(control,text='Median blur')

def brightnessChange(event):
    global img,beta
    beta=brightness.get()
    editImg()
brightness = Scale(control,from_=-100,to=100,orient='horizontal',command=brightnessChange)

def contrastChange(event):
    global img,alpha
    alpha=contrast.get()/10
    editImg()
contrast = Scale(control,from_=0,to=20,orient='horizontal',command=contrastChange)

def gamChange(event):
    global img,gamma
    gamma = gamCorrect.get()/100
    editImg()
gamCorrect = Scale(control,from_=0,to=2500,orient='horizontal',command=gamChange)

def blurChange(event):
    global img,blurLvl
    blurLvl = blur.get()*2+1
    editImg()
blur = Scale(control,from_=0,to=15,orient='horizontal',command=blurChange)

def gauBlurChange(event):
    global img,gauBlurLvl
    gauBlurLvl = gausBlur.get()*2+1
    editImg()
gausBlur = Scale(control,from_=0,to=20,orient='horizontal',command=gauBlurChange)

def medBlurChange(event):
    global img,medBlurLvl
    medBlurLvl = medBlur.get()*2+1
    editImg()
medBlur = Scale(control,from_=0,to=15,orient='horizontal',command=medBlurChange)

def reset():
    loadDefault()
    editImg()
resetBtn = Button(control,text="Reset",command=reset)

def loadDefault():
    global alpha,beta,gamma
    global blurLvl,gauBlurLvl,medBlurLvl

    alpha=1
    beta=0
    gamma=1
    blurLvl = 1
    gauBlurLvl = 1
    medBlurLvl = 1

    brightness.set(0)
    contrast.set(10)
    gamCorrect.set(100)
    blur.set(0)
    gausBlur.set(0)
    medBlur.set(0)

loadDefault()

brightTitle.pack(side=TOP)
brightness.pack(side=TOP)
contrastTitle.pack(side=TOP)
contrast.pack(side=TOP)
gamCorrectTitle.pack(side=TOP)
gamCorrect.pack(side=TOP)
blurTitle.pack(side=TOP)
blur.pack(side=TOP)
gausTitle.pack(side=TOP)
gausBlur.pack(side=TOP)
medTitle.pack(side=TOP)
medBlur.pack(side=TOP)
resetBtn.pack()

#
# App behaviour
#

def setSettingState(state):
    brightness['state'] = state
    contrast['state'] = state
    gamCorrect['state'] = state
    blur['state']=state
    gausBlur['state']= state
    medBlur['state']= state

setSettingState('disabled')
saving=""
zoom = 700

def openImg():
    global rootImg,img,act,saving,zoom
    filetype=[("JPEG Files",["*.jpg","*.jpeg","*.jpe"]),
        ("Windows Bitmap",["*.bmp","*.dib"]),
        ("Portable Network Graphics","*.png"),
        ("WebP","*.webp"),
        ("Portable image format",["*.pbm", "*.pgm", "*.ppm", "*.pxm", "*.pnm"] ),
        ("PFM files","*.pfm"),
        ("Sun rasters",["*.sr", "*.ras"]),
        ("TIFF files", ["*.tiff", "*.tif"]),
        ("OpenEXR Image files","*.exr"),
        ("Radiance HDR",["*.hdr", "*.pic"]),
        ("All files","*")]
    file = askopenfilename(filetypes=filetype)
    if file is None: return
    im = cv.imread(file,1)

    if im is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    act=False
    setSettingState('normal')
    saving=""
    zoom = 700
    img = im
    rootImg = im
    renderImg()
    loadDefault()

def renderImg():
    global imgDisp,zoom,img,rootImg

    im=None
    (h,w,d)=rootImg.shape
    if (h>=w):
        r = zoom / h
        dim = (int(w * r), zoom)
        im = cv.resize(img,dim)
    else:
        r = zoom * 10 /7  / w
        tmp=math.floor(zoom*10/7)
        dim = (tmp, int(h * r))
        im = cv.resize(img,dim)

    b,g,r = cv.split(im)
    im=cv.merge((r,g,b))
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(im))
    imgDisp.configure(image=imgtk)
    imgDisp.image=imgtk  

def close():
    global img,act
    if act:
        quest = messagebox.askyesno('Close file',"You have't saved the file. Do you want to close it anyway?")
        if quest: realClose()
    else: realClose()
        
def realClose():
    global saving,imgDisp,act,img,placeholder,rootImg

    img=None
    rootImg=None
    act=False
    saving=""
    loadDefault()
    setSettingState('disabled')
    imgDisp.configure(image=placeholder)
    imgDisp.image=placeholder

def save():
    global saving,img,act
    act=False

    if img is None:
        messagebox.showerror("Error", "No image to save.")
        return

    if (saving==""): saveAs()
    else: cv.imwrite(saving,img)

def saveAs():
    global img,saving,act
    act=False

    if img is None:
        messagebox.showerror("Error", "No image to save.")
        return

    files = [('JPEG Files','*.jpg'),("All files","*")]
    place = asksaveasfile(mode='w', filetypes=files, defaultextension="*.jpg")
    if place is None: return
    saving=place.name
    cv.imwrite(saving,img)

def exit():
    if img is not None and act==True:
        quest = messagebox.askyesno('Quit app',"You have't saved the file. Do you want to quit app anyway?")
        if quest: app.destroy()
    else: app.destroy()

def about():
    messagebox.showinfo('About','Made by Khanh Nguyen in 2021.')

#
# Menubar
#

menubar = Menu(app)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openImg, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=save, accelerator="Ctrl+S")
filemenu.add_command(label="Save As", command=saveAs, accelerator="Ctrl+Shift+S")
filemenu.add_command(label="Close", command=close, accelerator="Ctrl+W")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit, accelerator="Ctrl+Q")

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", accelerator="F1")
helpmenu.add_command(label="About", command=about)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Help", menu=helpmenu)

#
# Events
#

isCtrl=False

def keyPressed(e):
    global isCtrl
    if (e.keysym=='Control_L' or e.keysym=='Control_R'): isCtrl = True

def keyRelease(e):
    global isCtrl
    if (e.keysym=='Control_L' or e.keysym=='Control_R'): isCtrl = False

def scroll(e):
    global isCtrl,zoom
    if isCtrl: 
        zoom+=e.delta
        renderImg()

thick =7
penColor = (0,0,0)
curX=0
curY=0
def mouseDownMoved(e):
    global img,zoom,thick,penColor,curX,curY,rootImg
    (h,w,d)=img.shape

    if (curX==0 and curY==0):
        curX=e.x
        curY=e.y
        return

    if (h>=w):
        nw=zoom/h*w
        x=math.floor(e.x/nw*w)
        y=math.floor(e.y/zoom*h)

        bx=math.floor(curX/nw*w)
        by=math.floor(curY/zoom*h)

        r=math.floor(thick/zoom*h)
        cv.line(rootImg,(bx,by),(x,y),penColor,r)
    else:
        tmp=zoom*10/7
        nh=tmp/w*h
        x=math.floor(e.x/tmp*w)
        y=math.floor(e.y/nh*h)

        bx=math.floor(curX/tmp*w)
        by=math.floor(curY/nh*h)

        r=math.floor(thick/tmp*w)
        cv.line(rootImg,(bx,by),(x,y),penColor,r)

    curX=e.x
    curY=e.y
    editImg()

def mouseUp(e):
    global curX,curY
    curX=0
    curY=0

imgDisp.bind('<B1-Motion>',mouseDownMoved)
imgDisp.bind('<ButtonRelease-1>',mouseUp)

app.bind('<Key>', keyPressed)
app.bind('<KeyRelease>', keyRelease)
app.bind('<MouseWheel>',scroll)
app.config(menu=menubar)
app.mainloop()