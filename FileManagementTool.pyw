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
master.title("Sesock File Management Tool v0.0.4")
left_edge = master.winfo_screenwidth()/3
top_edge = master.winfo_screenheight()/3
master.geometry('%dx%d+250+250' %(500, 560))
master.resizable(False, False)

s = ttk.Style(master)
master.tk.call('source', 'forest-dark.tcl')
s.theme_use('forest-dark')

BUTTON_WIDTH = 18
#label_font = Font(size=8, weight='bold', family="Consolas")

master.bind('<Control-c>', lambda event: console.delete(1.0, "end"))
master.bind('<F1>', lambda event: aboutDialog())

try:
    dirp = os.path.dirname(__file__)
    photo = PhotoImage(file="assets\\IconSmall.png")
    master.iconphoto(False, photo)
except:
    pass

full_directory = os.getcwd()
text = tk.StringVar()
text.set(full_directory[-50:])

TAB_CONTROL = ttk.Notebook(master)
tabBasicOperations = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabBasicOperations, text="Basic Tools")
tabAdvancedOperations = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabAdvancedOperations, text="Advanced Tools")
tabSettings = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabSettings, text="Settings")

TAB_CONTROL.pack(expand=1, fill="both")
currentDirectory = ttk.Label(tabBasicOperations, text="Current Directory: ").place(x=20, y=20)
directoryText = ttk.Label(tabBasicOperations, textvariable=text).place(x=130, y=20)

#Interface buttons
#Column 1
renameButton = ttk.Button(tabBasicOperations, text="Rename Files", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:renameFiles()).place(x=80, y=60)
organizeButton = ttk.Button(tabBasicOperations, text="Organize Files", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:organizeFiles()).place(x=80, y=95)
moveupButton = ttk.Button(tabBasicOperations, text="Move Files Up", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:moveupFiles()).place(x=80, y=130)
backupButton = ttk.Button(tabBasicOperations, text='Backup Files', width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:backupFiles()).place(x=80, y=165)
#compressButton = ttk.Button(tabBasicOperations,text='Zip Files', width=BUTTON_WIDTH, command=lambda:compressFiles()).place(x=40, y=180)
#Column 3
directoryButton = ttk.Button(tabBasicOperations, text="Change Directory...", width=BUTTON_WIDTH, command=lambda:changeDirectory()).place(x=250, y=60)
listfilesButton = ttk.Button(tabBasicOperations,text='List Files', width=BUTTON_WIDTH, command=lambda:listFiles()).place(x=250, y=95)
clearConsoleButton = ttk.Button(tabBasicOperations, text="Clear Console", width=BUTTON_WIDTH, command=lambda:clearConsole()).place(x=250, y=130)
resetDirectoryButton = ttk.Button(tabBasicOperations, text="Reset Directory", width=BUTTON_WIDTH, command=lambda:resetDirectory()).place(x=250, y=165)
#fileCountButton = ttk.Button(tabBasicOperations, text="File Count", width=BUTTON_WIDTH, command=lambda:outputFileCount()).place(x=326, y=180)
#Console
console = tkscrolled.ScrolledText(height=15, width=65, foreground='white', undo=True)
console.place(x=10, y=250)
#Progress Bar
progress = ttk.Progressbar(master, orient=HORIZONTAL, length=480, mode='determinate').place(x=10, y=505)

#Settings Buttons
defaultDirectoryLabel = ttk.Label(tabSettings, text="Default Directory:").place(x=30, y=55)
defaultDirectory = ttk.Entry(tabSettings, width=40)
defaultDirectory.place(x=140, y=50)
defaultDirectory.insert(0, full_directory)

defaultBackupLabel = ttk.Label(tabSettings, text="Default Backup:").place(x=30, y=95)
defaultBackup = ttk.Entry(tabSettings, width=40)
defaultBackup.place(x=140, y=90)
defaultBackup.insert(0, full_directory+'\\backup')

#Batch renaming of files
def renameFiles(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, 'Renaming Files...\n')

    directory = full_directory
    to_be_named = os.listdir(path = directory)

    total = getFileCount()
    counter = 2.0
    for i in range(0, len(to_be_named)):
        extension = os.path.splitext(to_be_named[i])[1]
        filename = str(i+1)+'-'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))+extension
        os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, filename))
        #load(3)
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
    console.insert(1.0, "Count \tFilename \t\tFiletype\n")
    for file in files:
        filename = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]
        console.insert(counter, str(line_number)+")\t"+filename+'\t\t'+extension+'\n')
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
    text.set(filename[-50:])
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
    text.set(full_directory[-50:])
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
    dialog = """ Author: Chris Sesock \n Version: 0.0.3 \n Commit: 077788d6166f5d69c9b660454aa264dd62956fb6 \n Date: 2020-11-06:12:00:00 \n Python: 3.8.3 \n OS: Windows_NT x64 10.0.10363
             """
    messagebox.showinfo("About", dialog)

if __name__ == '__main__':
    master.mainloop()