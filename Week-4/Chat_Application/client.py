import socket
import threading
import tkinter as tk
from tkinter import END, NORMAL, DISABLED, CENTER
from chat import format_message

PORT = 5000
SERVER = '192.168.16.26'
FORMAT = 'utf-8'
EXIT_MESSAGE = "!EXIT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

class GUI:
    def __init__(self):
        self.Window = tk.Tk()
        self.Window.withdraw()

        # Login window
        self.login = tk.Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = tk.Label(self.login, text="Enter your Name to continue", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelName = tk.Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryName = tk.Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        self.go = tk.Button(self.login, text="Enter", font="Helvetica 14 bold",bg="#ffae00", command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("Chat-Room")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#000d57")

        self.labelHead = tk.Frame(self.Window, bg="#000d57", bd=2)
        self.labelHead.place(relwidth=1)

        self.labelName = tk.Label(self.labelHead, bg="#000d57", fg="#fff", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelName.pack(side=tk.LEFT, padx=10)

        self.exitButton = tk.Button(self.labelHead, text="Exit", font="Helvetica 10 bold", bg="#e74c3c", fg="#fff", command=self.on_closing)
        self.exitButton.pack(side=tk.RIGHT, padx=10)

        self.line = tk.Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = tk.Text(self.Window, width=20, height=2, bg="#006eec", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = tk.Label(self.Window, bg="#000d57", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = tk.Entry(self.labelBottom, bg="#fff", fg="#000", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg="#001fbc", fg="#fff",command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occurred!")
                client.close()
                break

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = self.msg
            formatted_message = format_message(self.name, message)
            client.send(formatted_message.encode(FORMAT))
            break

    def on_closing(self):
        client.send(EXIT_MESSAGE.encode(FORMAT))
        self.Window.destroy()
        client.close()

g = GUI()
