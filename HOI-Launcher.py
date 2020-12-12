#! /usr/bin/env python
import os
import subprocess
import pathlib

def walklevel(path, depth = 1):
    if depth < 0:
        for root, dirs, files in os.walk(path):
            yield root, dirs[:], files
        return
    elif depth == 0:
        return
    base_depth = path.rstrip(os.path.sep).count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs[:], files
        cur_depth = root.count(os.path.sep)
        if base_depth + depth <= cur_depth:
            del dirs[:]

launcherdir = str(pathlib.Path(__file__).parent.absolute())
gamedir = launcherdir[0:launcherdir.index("launcher")]

mods = {}
paths = []
foo = [x[0] for x in walklevel(gamedir+"mods", 1)]
for x in foo:
    mods[x] = {
        "name": "", "desc": "", "author": "", "base": "False"
    }
    mods[x]["path"] = x
    paths.append(x)
    filepath = x+"/descriptor.mod"
    with open(filepath) as fp:
        lines = fp.readlines()
        for line in lines:
            line = line[0:-1].split("=")
            mods[x][line[0]] = line[1] 
    if mods[x]["name"] == "":
        mods[x]["name"] = x.replace(gamedir, "").replace("mods/", "")

def rungame(modindex):
    window.destroy()
    if mods[paths[modindex]]["base"] == "True":
        bashcommand = "cd \"{}\"; wine HoI.exe".format(gamedir)
    else:
        bashcommand = "cd \"{}\"; wine ../../HoI.exe".format(paths[modindex]+"/")
    print(bashcommand)
    os.system(bashcommand)

modnames = [mods[x]["name"] for x in mods]

def settext():
    desc.configure(state="normal")
    desc.delete(1.0, END)
    desctext = mods[paths[cb.current()]]["desc"]
    desc.insert(END, desctext)
    desc.configure(state="disabled")

from tkinter import *
from tkinter.ttk import Combobox
window=Tk()

photo = PhotoImage(file = "bg.png")
w = Label(window, image=photo)
w.pack()

cb=Combobox(window, values=modnames, state="readonly")
cb.bind('<<ComboboxSelected>>', lambda _ : settext())
cb.current(0)
cb.place(x=120,y=140,w=240)

desctext = StringVar()
desc=Text(window, state="disabled")
desc.insert(END, desctext)
settext()
desc.place(x=80,y=165,w=320, h=150)

bt=Button(window, text="Launch Game", command=lambda: rungame(cb.current()))
bt.pack()
bt.place(x=192, y=320, w=96, h=32)

window.title("Hearts of Iron Launcher")
window.geometry("480x360")
window.mainloop()
