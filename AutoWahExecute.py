from tkinter import *
import AutoWah


vari = True
tk = Tk()
tk.title("AutoWah")
def validate():
    AutoWah.renderAutowah(
        file = fileIn.get(),
        maximum = maxi.get(),
        minimum = mini.get(),
        peak = vari,
        p = p.get(),
        write=True,
        output=fileOut.get())

def peakState():
    global vari
    vari = not vari


lowpass = Frame(height=2, bd=1, relief=SUNKEN)
mini = Scale(lowpass, from_=10000, to=100, length = 200, label="Min Frequency")
maxi = Scale(lowpass, from_=10000, to=100, length = 200, label="Max Frequency")
lowpass.pack(fill=X, padx=5, pady=5)
mini.pack(side = LEFT )
maxi.pack(side = LEFT )

resonant = Frame(height=10, bd=1, relief=SUNKEN)
peak = Checkbutton(resonant, text="Peak", command = peakState)
peak.select()
p = Scale(resonant, from_=1, to=0, resolution = 0.01, label="Peak Height")
p.set(1)
resonant.pack(fill=X, padx=5, pady=5)
peak.pack(side = LEFT )
p.pack(side = LEFT )


file = Frame(height=2, bd=1, relief=SUNKEN)
fileIn = Entry(file, width = 30)
fileOut = Entry(file, width = 30)
labelIn = Label(file, text="Input file")
labelOut = Label(file, text="Save to")
b = Button(file, text="OK", command=validate, width = 10)
file.pack(fill=X, padx=5, pady=5)
labelIn.grid(row = 0,column = 0)
fileIn.grid(row = 0,column = 1)
labelOut.grid(row = 1,column = 0)
fileOut.grid(row = 1,column = 1)
b.grid(row = 1,column = 2, padx = 10)





