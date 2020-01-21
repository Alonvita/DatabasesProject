from tkinter import *
from View import login_page, preferences_page
from Logic import GameLogic as gL


def register_window(window, fileBackground, fileBackground2):
    for widget in window.winfo_children():
        widget.destroy()
    background_label = Label(window, image=fileBackground)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window, bg="light blue")
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='Register', fg='black', bg="light blue", font=("Comic Sans MS", 20, "bold"))
    name.grid(row=0, columnspan=2, pady=(10, 10))

    nameL = Label(frame, text='Username: ', bg="light blue", font=("Comic Sans MS", 12))  # More labels
    pwordL = Label(frame, text='Password: ', bg="light blue", font=("Comic Sans MS", 12))  # ^
    nameL.grid(row=1, column=0, padx=(10, 0))
    pwordL.grid(row=2, column=0, padx=(10, 0))

    username = StringVar()
    password = StringVar()
    nameEL = Entry(frame, textvariable=username)  # The entry input
    pwordEL = Entry(frame, show='*', textvariable=password)
    nameEL.grid(row=1, column=1, padx=(0, 10))
    pwordEL.grid(row=2, column=1, padx=(0, 10))

    bottonSend = Button(frame, text='Register', bg="#10c716", fg="black", width=12, font=("Comic Sans MS", 12),
                        command=lambda: validateRegister(window, frame, username, password, fileBackground, fileBackground2))
    bottonSend.grid(row=3, columnspan=2, pady=(10, 5))

    bottonLogin = Button(frame, text='Login Page', fg="black",width=12, font=("Comic Sans MS", 12),
                         command=lambda: login_page.login_window(window, fileBackground, fileBackground2))
    bottonLogin.grid(row=4, columnspan=2, pady=(0, 10))


def validateRegister(window, frame, name, pword, fileBackground, fileBackground2):
    print(name.get(), pword.get())
    validateR = gL.register(name.get(), pword.get())
    if validateR == 0:
        label = Label(frame, text='User Exists!', fg='red', bg="light blue", font=("Comic Sans MS", 12))
        label.grid(row=5, columnspan=2, pady=(5, 5))
    if validateR == 1:
        label = Label(frame, text='Please enter only 6-12 chars in password!', fg='red', bg="light blue", font=("Comic Sans MS", 12))
        label.grid(row=5, columnspan=2, pady=(5, 5))
    if validateR == 2:
        label = Label(frame, text='Please enter at least 2 chars in username!', fg='red', bg="light blue", font=("Comic Sans MS", 12))
        label.grid(row=5, columnspan=2, pady=(5, 5))
    else:
        preferences_page.preference_window(window, name, fileBackground, fileBackground2)
