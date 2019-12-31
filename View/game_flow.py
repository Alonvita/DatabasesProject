from tkinter import *
from View import login_page

window = Tk()
window.title("The memory game of a funny name")
window.geometry("800x600")
window.minsize(width=800, height=600)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(1, weight=1)

backgroundName = sys.path[0] + '\\background.png'
fileBackground = PhotoImage(file=backgroundName)

#window.resizable(True, True)
login_page.login_window(window, fileBackground)
window.mainloop()
