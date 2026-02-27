import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("LAN Messenger Pro")
        self.root.geometry("800x500")
        self.root.minsize(700, 450)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.nickname = simpledialog.askstring("Nickname", "Enter nickname:", parent=root)
        if not self.nickname:
            root.destroy()
            return

        try:
            self.sock.connect((HOST, PORT))
        except:
            messagebox.showerror("Connection Error", "Server not reachable")
            root.destroy()
            return

        self.selected_user = None  # 👈 private chat target

        self.build_layout()
        threading.Thread(target=self.receive_loop, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- UI LAYOUT ----------
    def build_layout(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = tk.Frame(self.root, bg="#1e1e1e", width=180)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="ONLINE",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=10)

        self.user_list = tk.Listbox(
            sidebar,
            bg="#2b2b2b",
            fg="white",
            bd=0,
            highlightthickness=0
        )
        self.user_list.pack(fill="both", expand=True, padx=10, pady=5)

        # detect click for private chat
        self.user_list.bind("<<ListboxSelect>>", self.on_user_select)

        # Chat area container
        chat_frame = tk.Frame(self.root, bg="#252526")
        chat_frame.grid(row=0, column=1, sticky="nsew")

        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_canvas = tk.Canvas(chat_frame, bg="#252526", highlightthickness=0)
        self.chat_canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.chat_canvas.configure(yscrollcommand=scrollbar.set)

        self.messages_frame = tk.Frame(self.chat_canvas, bg="#252526")
        self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        self.messages_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )
        )

        # Input area
        input_frame = tk.Frame(self.root, bg="#1e1e1e", height=60)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.msg_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bd=0
        )
        self.msg_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.msg_entry.bind("<Return>", self.send_message)

        send_btn = tk.Button(
            input_frame,
            text="Send",
            bg="#0078D7",
            fg="white",
            bd=0,
            padx=20,
            command=self.send_message
        )
        send_btn.grid(row=0, column=1, padx=10)

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Connected",
            anchor="w",
            bg="#0078D7",
            fg="white"
        )
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew")

    # ---------- USER CLICK ----------
    def on_user_select(self, event):
        sel = self.user_list.curselection()
        if sel:
            self.selected_user = self.user_list.get(sel[0])
        else:
            self.selected_user = None

    # ---------- MESSAGE BUBBLES ----------
    def add_message(self, text, sender="other"):
        time_str = datetime.now().strftime("%H:%M")

        container = tk.Frame(self.messages_frame, bg="#252526")
        container.pack(fill="x", pady=2, padx=10)

        if sender == "self":
            anchor = "e"
            bg = "#0078D7"
            fg = "white"
        elif sender == "server":
            anchor = "center"
            bg = "#444"
            fg = "white"
        else:
            anchor = "w"
            bg = "#2b2b2b"
            fg = "white"

        bubble = tk.Label(
            container,
            text=f"{text}  {time_str}",
            bg=bg,
            fg=fg,
            wraplength=400,
            justify="left",
            padx=10,
            pady=6
        )
        bubble.pack(anchor=anchor)

        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1)

    # ---------- SEND ----------
    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return

        try:
            # private
            if self.selected_user:
                payload = f"@{self.selected_user}|{msg}"
                self.sock.send(payload.encode())
                self.add_message(f"[PM → {self.selected_user}] {msg}", "self")
            else:
                self.sock.send(msg.encode())
                self.add_message(f"{self.nickname}: {msg}", "self")

        except:
            pass

        self.msg_entry.delete(0, "end")

    # ---------- RECEIVE ----------
    def receive_loop(self):
        while True:
            try:
                msg = self.sock.recv(1024)
                if not msg:
                    break

                if msg == b"NICK":
                    self.sock.send(self.nickname.encode())

                elif msg.startswith(b"USERLIST:"):
                    users = msg.decode().split(":")[1].split(",")
                    self.update_user_list(users)

                else:
                    text = msg.decode()

                    if text.startswith("[SERVER]"):
                        self.add_message(text, "server")
                    elif text.startswith("[PM]"):
                        self.add_message(text, "other")
                    else:
                        self.add_message(text, "other")

            except:
                break

        self.sock.close()
        self.status.config(text="Disconnected")

    # ---------- USERS ----------
    def update_user_list(self, users):
        self.user_list.delete(0, "end")
        for u in users:
            if u and u != self.nickname:
                self.user_list.insert("end", u)

    # ---------- CLOSE ----------
    def on_close(self):
        try:
            self.sock.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()