# 💬 LAN Chat Room with Private Messaging (Python & Tkinter)

A GUI-based LAN chat room application built using Python sockets and Tkinter.  
Multiple users on the same local network can communicate in real time with support for private messaging and live user presence.

---

## 📖 Overview

This project implements a desktop chat room operating entirely over a local network (LAN).  
It follows a client–server architecture where a central Python socket server routes messages between connected GUI clients.

👤 Users can:
- Join a shared chat room  
- View online participants  
- Send public messages  
- Send private messages by selecting a user  

The system is lightweight, dependency-minimal, and designed as a foundation for advanced LAN collaboration tools.

---

## ✨ Features

- 🧑‍🤝‍🧑 Multi-client LAN chat room  
- 🖥️ Tkinter GUI client  
- 📡 Real-time message broadcasting  
- 🔒 Private messaging (user-to-user)  
- 📋 Live online user list  
- 🔔 Join/leave notifications  
- ⚙️ Threaded socket server  
- 🌙 Clean dark chat UI  

---

## 🏗️ Architecture


::contentReference[oaicite:0]{index=0}


**Flow**

Client → TCP → Server → TCP → Other Clients  

Server acts as a routing hub for:
- public broadcasts  
- private messages  
- presence updates  

---

## 🗂️ Project Structure

```

LAN-Chat-Room/
│
├── server.py            # Socket server (routing + presence)
├── client.py            # Tkinter GUI chat client
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── .gitignore

````

---

## ⚙️ Requirements

- Python 3.8+
- Tkinter

### Linux
```bash
sudo apt install python3-tk
````

### Windows / macOS

Tkinter is included with Python.

---

## 🚀 Installation

```bash
git clone https://github.com/Srikumaran5557/LAN-Chat-Room.git
cd LAN-Chat-Room
```

---

## ▶️ How to Run

### 1️⃣ Start Server

```bash
python server/server.py
```

Server listens on local IP at **port 5050**.

---

### 2️⃣ Start Client

```bash
python client/client.py
```

Enter nickname when prompted.

Run multiple clients on different machines (same LAN).

---

## 🔒 Private Messaging

1. Click a username in the **ONLINE** list
2. Type message
3. Press Send

Only the selected user receives the message.

---

## 🌐 Networking Details

* Protocol: TCP sockets
* Port: 5050
* Encoding: UTF-8 text
* Concurrency: thread per client
* Presence: server-broadcast user list

---

## ⚠️ Limitations

* LAN only (no internet routing)
* No message persistence
* No file transfer yet
* No encryption
* Single chat room

---

## 🔮 Future Enhancements

* 📎 File sharing
* 🖥️ Screen sharing
* 💾 Message history (SQLite)
* 🧩 Multiple rooms
* 😀 Emojis & attachments
* 🧑‍🎨 User avatars
* 🟢 Online/offline status
* 🔐 Encryption

---

```
