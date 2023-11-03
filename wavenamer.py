from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import wave
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
import os
import re
root = Tk()
root.title("Wave Namer")
root.filename = "insert file"
root.out_filename = ""
outf = StringVar()
infi = StringVar()
stat = StringVar()
stat.set("Status: Please select input and output files")
dir_path = os.path.dirname(os.path.realpath(__file__))
#app_path, rest = re.split(r"/[^/]*\.app/", dir_path, 1)
#if not os.path.isdir( app_path + "/sortedsounds/"):
#    os.makedirs(app_path + "/sortedsounds/")


def out_folder():
    root.out_filename = filedialog.askdirectory()
    outf.set(root.out_filename)

def folderopen():
    global fi_list
    fi_list.configure(state="normal")
    root.filename = filedialog.askdirectory()
    mydir = root.filename
    if mydir == '':
        return None
    infi.set(root.filename)
    file_list = glob.glob(mydir)
    file_list.extend(glob.glob(mydir + "**/*.wav", recursive =True))
    print("FILE_LIST", file_list)
    for fi in file_list[1:]:
        ex = wave.open(fi, "r")
        bits = ex.getsampwidth() * 8
        bound = 2 ** (bits - 1) - 1
        ex_p = np.frombuffer(ex.readframes(ex.getnframes()), dtype = np.int16).copy()
        sp = np.fft.rfft(ex_p)
        print(np.where(sp == max(sp)))
        ex.close()
        fi_list.insert(END, str(fi) + "\n" + "renamed and copied to" + "\n" + root.out_filename + "/" + str( np.where(sp == max(sp))[0][0]) + "_" + os.path.basename(fi) + "\n")    
        with open(fi, 'rb') as input:
            output = open(root.out_filename + "/" + str( np.where(sp == max(sp))[0][0]) + "_" + os.path.basename(fi), 'wb')
            output.write(input.read())
        input.close()
        output.close()
    fi_list.configure(state="disabled")
    stat.set("Status: Complete")

fi_list = scrolledtext.ScrolledText(root, height = 5, width = 52)


lb3 = Label(root, wraplength=300, justify=LEFT, text="Welcome to Wave Namer! Select an output folder to collect the renamed files in. Then select a folder of .wav files for Wave Namer to read and rename.").pack()


btn = Button(root, text="Select an output folder", command = out_folder).pack()
lb = Label(root, wraplength=300, justify=LEFT, textvariable = outf ).pack()

btn = Button(root, text="Select a folder of .wav files", command = folderopen).pack()
lb2 = Label(root, wraplength=300, justify=LEFT, textvariable = infi ).pack()

lbstat = Label(root, wraplength=300, justify=LEFT, textvariable = stat).pack()

fi_list.pack()
fi_list.configure(state="disabled")

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
