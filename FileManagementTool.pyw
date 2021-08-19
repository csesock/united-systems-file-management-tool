import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.scrolledtext as tkscrolled
from tkinter.filedialog import askopenfilename
from tkinter.font import Font 
import os, shutil
from os import rename, listdir
import time
import random
import string 
from time import sleep

master = tk.Tk()
master.title("Sesock File Management Tool v0.0.5")
left_edge = master.winfo_screenwidth()/3
top_edge = master.winfo_screenheight()/3
master.geometry('%dx%d+250+250' %(500, 560))
master.resizable(False, False)

s = ttk.Style(master)
master.tk.call('source', 'forest-dark.tcl')
s.theme_use('forest-dark')

BUTTON_WIDTH = 17

master.bind('<Control-c>', lambda event: console.delete(1.0, "end"))
master.bind('<F1>', lambda event: aboutDialog())

try:
    photo = PhotoImage(file="assets\\IconSmall.png")
    master.iconphoto(False, photo)
except:
    pass

full_directory = os.getcwd()
text = tk.StringVar()
text.set(full_directory[-48:])

TAB_CONTROL = ttk.Notebook(master)
tabBasicOperations = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabBasicOperations, text="Basic Tools")
tabAdvancedOperations = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabAdvancedOperations, text="Advanced Tools")
tabSettings = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabSettings, text="Settings")

TAB_CONTROL.pack(expand=1, fill="both")
currentDirectory = ttk.Label(tabBasicOperations, text="Current Directory: ").place(x=20, y=20)
directoryText = ttk.Label(tabBasicOperations, textvariable=text, foreground="white").place(x=130, y=20)

#Interface buttons
#Column 1
renameButton = ttk.Button(tabBasicOperations, text="Rename Files", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:renameFiles()).place(x=20, y=60)
organizeButton = ttk.Button(tabBasicOperations, text="Organize Files", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:organizeFiles()).place(x=20, y=95)
moveupButton = ttk.Button(tabBasicOperations, text="Move Files Up", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:moveupFiles()).place(x=20, y=130)
backupButton = ttk.Button(tabBasicOperations, text='Backup Files', width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:backupFiles()).place(x=20, y=165)
#compressButton = ttk.Button(tabBasicOperations,text='Zip Files', width=BUTTON_WIDTH, command=lambda:compressFiles()).place(x=40, y=180)
#Column 3
directoryButton = ttk.Button(tabBasicOperations, text="Change Directory...", width=BUTTON_WIDTH, command=lambda:changeDirectory()).place(x=180, y=60)
listfilesButton = ttk.Button(tabBasicOperations,text='List Files', width=BUTTON_WIDTH, command=lambda:listFiles()).place(x=180, y=95)
clearConsoleButton = ttk.Button(tabBasicOperations, text="Clear Console", width=BUTTON_WIDTH, command=lambda:clearConsole()).place(x=180, y=130)
resetDirectoryButton = ttk.Button(tabBasicOperations, text="Reset Directory", width=BUTTON_WIDTH, command=lambda:resetDirectory()).place(x=180, y=165)
#fileCountButton = ttk.Button(tabBasicOperations, text="File Count", width=BUTTON_WIDTH, command=lambda:outputFileCount()).place(x=326, y=180)

check_frame = ttk.LabelFrame(master, text="Options").place(x=320, y=60)
check_1 = ttk.Checkbutton(check_frame, text="Unchecked")

# Create a Frame for the Radiobuttons
radio_frame = ttk.LabelFrame(tabBasicOperations, text="Name Schema", padding=(5, 5))
radio_frame.place(x=350, y=53)
d = tk.IntVar(value=3)
# Radiobuttons
radio_1 = ttk.Radiobutton(radio_frame, text="Integers", variable=d, value=1)
radio_1.grid(row=0, column=0, padx=5, pady=6, sticky="nsew")
radio_2 = ttk.Radiobutton(radio_frame, text="Hashes", variable=d, value=2)
radio_2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
radio_3 = ttk.Radiobutton(radio_frame, text="Mixed", variable=d, value=3)
#radio_3.state(["alternate"])
radio_3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")


#Console
console = tkscrolled.ScrolledText(height=15, width=65, foreground='white', background='black', undo=True)
console.place(x=10, y=280)
#Progress Bar
#progress = ttk.Progressbar(master, orient=HORIZONTAL, length=480, mode='determinate').place(x=10, y=505)

length_label1 = ttk.Label(text="Lines : ", foreground='#52565e').place(x=10, y=530)
length_text = tk.StringVar()
length_text.set("0")
length_label = ttk.Label(textvariable=length_text, foreground='#52565e').place(x=55, y=530)

length_label2 = ttk.Label(text="Length : ", foreground='#52565e').place(x=85, y=530)
length_text2 = tk.StringVar()
length_text2.set("0")
length_label2 = ttk.Label(textvariable=length_text2, foreground='#52565e').place(x=140, y=530)

system_label = ttk.Label(text="win32", foreground="#52565e").place(x=452, y=530)

# tv = ttk.Treeview(master, show='tree')
# tv.place(x=50, y=50)
# tv.heading('#0',text='Dir：'+full_directory,anchor='w')
# path=os.path.abspath(full_directory)
# node=tv.insert('','end',text=path,open=True)
# def traverse_dir(parent,path):
#     for d in os.listdir(path):
#         full_path=os.path.join(path,d)
#         isdir = os.path.isdir(full_path)
#         id=tv.insert(parent,'end',text=d,open=False)
#         if isdir:
#             traverse_dir(id,full_path)
# traverse_dir(node,path)
# tv.pack()

#Settings Buttons
defaultDirectoryLabel = ttk.Label(tabSettings, text="Default Directory:").place(x=30, y=55)
defaultDirectory = ttk.Entry(tabSettings, width=40)
defaultDirectory.place(x=160, y=50)
defaultDirectory.insert(0, full_directory)

defaultBackupLabel = ttk.Label(tabSettings, text="Default Backup:").place(x=30, y=95)
defaultBackup = ttk.Entry(tabSettings, width=40)
defaultBackup.place(x=160, y=90)
defaultBackup.insert(0, full_directory+'\\backup')

defaultHashLengthLabel = ttk.Label(tabSettings, text="Default Hash Length:").place(x=30, y=135)
defaultHashLength = ttk.Entry(tabSettings, width=5)
defaultHashLength.place(x=160, y=130)
defaultHashLength.insert(0, '10')

#Batch renaming of files
def renameFiles(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, 'Renaming Files...\n')

    directory = full_directory
    to_be_named = os.listdir(path = directory)

    total = getFileCount()
    counter = 2.0
    if d.get() == 3: #mix of hashes and numbers
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = str(i+1)+'-'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(int(defaultHashLength.get())))+extension
            os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, filename))
            console.insert(counter, "Renaming file "+str(i)+" of "+str(total)+"\n")
            counter+=1     
        console.insert(counter, "Files successfully renamed")
    elif d.get() == 2: # just hashes
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(int(defaultHashLength.get())))+extension
            os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, filename))
            console.insert(counter, "Renaming file "+str(i)+" of "+str(total)+"\n")
            counter+=1     
        console.insert(counter, "Files successfully renamed")
    else:
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = str(i+1)+extension
            os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, filename))
            console.insert(counter, "Renaming file "+str(i)+" of "+str(total)+"\n")
            counter+=1     
        console.insert(counter, "Files successfully renamed")

def organizeFiles(event=None):
    console.delete(1.0, "end")
    console.insert(1.0, "Organizing Files...")
    #shutil.move(path+'/'+file_, path+'/'+ext+'/'+file_)

#Moves all files in current directory up one level
def moveupFiles(event=None):
    filename = filedialog.askdirectory()
    for root, dirs, files in os.walk(filename, topdown=False):
        for file in files:
            try:
                shutil.move(os.path.join(root, file), filename)
            except OSError:
                pass

#Creates backup of files in current directory
def backupFiles(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, "Opening Backup File dialog...\n")

    filename = tk.filedialog.askopenfilename(title="Choose File to Backup")
    shutil.copy(filename, os.getcwd())

    console.insert(2.0, "Files successfully backed up")

#Compresses files in current directory
def compressFiles(event=None):
    filename = tk.filedialog.askopenfilename(title="Choose File to Compress")
    shutil.make_archive('compressed', 'zip', filename)

#Prints all files in current directory to console
def listFiles(event=None):
    line_number = 1
    files = os.listdir(full_directory)
    console.delete(1.0, 'end')
    counter = 2.0
    console.insert(1.0, "Count \tFilename\n")
    for file in files:
        filename = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]
        console.insert(counter, str(line_number)+")\t"+filename+'\n')
        counter+=1.0
        line_number+=1

#Changes current directory used by the tool
def changeDirectory(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, "Changing directory...\n")
    
    global full_directory
    filename = filedialog.askdirectory()
    if not filename:
        console.insert(2.0, "Operation cancelled\n")
        return 
    full_directory = filename 
    text.set(filename[-48:])
    console.insert(2.0, "Directory successfully changed\n")

#Returns int of file count
def getFileCount():
    list = os.listdir(full_directory)
    number = len(list)
    return number

#Outputs int of file count to console
def outputFileCount(event=None):
    list = os.listdir(full_directory)
    number = len(list)
    console.delete(1.0, 'end')
    console.insert(1.0, str(len(os.listdir(full_directory))))
    
def clearConsole(event=None):
    console.delete(1.0, "end")

def resetDirectory(event=None):
    console.delete(1.0, "end")
    global full_directory
    full_directory = os.getcwd()
    text.set(full_directory[-48:])
    console.insert(2.0, "Directory Reset")

def changeTheme(theme):
    s = ttk.Style()
    s.theme_use(theme)

def load(n):
    console.delete(1.0, 'end')
    for i in range(n):
        sleep(0.1)
        console.insert(1.0, f"{i/n*100:.1f} %", end="\r")  

def aboutDialog():
    dialog = """ Author: Chris Sesock \n Version: 0.0.5 \n Commit: 077788d6166f5d69c9b660454aa264dd62956fb6 \n Date: 2021--06:12:00:00 \n Python: 3.8.5 \n OS: Windows_NT x64 10.0.10363
             """
    messagebox.showinfo("About", dialog)

if __name__ == '__main__':
    master.mainloop()