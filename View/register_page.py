from tkinter import *
from View import login_page, preferences_page
from Logic import GameLogic as gL


# register page window- get the window and the background and show the register page
def register_window(window, fileBackground, fileBackground2):
    # destroy all the old widgets in the frame
    for widget in window.winfo_children():
        widget.destroy()
    # initialize the background
    background_label = Label(window, image=fileBackground)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    frame = Frame(window, bg="light blue")
    frame.grid(row=1, column=1)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    name = Label(frame, text='Register', fg='black', bg="light blue", font=("Comic Sans MS", 20, "bold"))
    name.grid(row=0, columnspan=2, pady=(10, 10))

    nameL = Label(frame, text='Username: ', bg="light blue", font=("Comic Sans MS", 12))
    pwordL = Label(frame, text='Password: ', bg="light blue", font=("Comic Sans MS", 12))
    nameL.grid(row=1, column=0, padx=(10, 0))
    pwordL.grid(row=2, column=0, padx=(10, 0))

    username = StringVar()
    password = StringVar()
    nameEL = Entry(frame, textvariable=username)  # The name input
    pwordEL = Entry(frame, show='*', textvariable=password)  # The password input
    nameEL.grid(row=1, column=1, padx=(0, 10))
    pwordEL.grid(row=2, column=1, padx=(0, 10))

    # register button
    bottonSend = Button(frame, text='Register', bg="#10c716", fg="black", width=12, font=("Comic Sans MS", 12),
                        command=lambda: validateRegister(window, frame, username, password, fileBackground,
                                                         fileBackground2))
    bottonSend.grid(row=3, columnspan=2, pady=(10, 5))

    # go to login page
    bottonLogin = Button(frame, text='Login Page', fg="black", width=12, font=("Comic Sans MS", 12),
                         command=lambda: login_page.login_window(window, fileBackground, fileBackground2))
    bottonLogin.grid(row=4, columnspan=2, pady=(0, 10))


# function that validate the login
def validateRegister(window, frame, name, pword, fileBackground, fileBackground2):
    validateR = gL.register(name.get(), pword.get())
    # 0 - user exist, -1- password not ok, -2-user name not ok, else- everything ok go to preference menu
    if validateR == 0:
        label = Label(frame, text='User Exists!', fg='red', bg="light blue", font=("Comic Sans MS", 12))
        label.grid(row=5, columnspan=2, pady=(5, 5))
        return
    elif validateR == -1:
        label = Label(frame, text='Please enter only 6-12 chars in password!', fg='red', bg="light blue",
                      font=("Comic Sans MS", 12))
        label.grid(row=5, columnspan=2, pady=(5, 5))
    elif validateR == -2:
        label = Label(frame, text='Please enter at least 2 chars in username!', fg='red', bg="light blue",
                      font=("Comic Sans MS", 12))
        label.grid(row=5, columnspan=2, pady=(5, 5))
    else:
        preferences_page.preference_window(window, name, fileBackground, fileBackground2)
