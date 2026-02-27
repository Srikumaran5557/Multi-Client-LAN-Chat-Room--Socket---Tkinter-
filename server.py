import socket
import threading

HOST =  socket.gethostbyname(socket.gethostname())
PORT = 5050

clients = {}
lock = threading.Lock()

def broadcast(message, sender=None):
    with lock:
        for conn in list(clients.keys()):
            if conn != sender:
                try:
                    conn.send(message)
                except:
                    remove_client(conn)

def send_private(sender_name, target_name, message):
    with lock:
        for conn, name in clients.items():
            if name == target_name:
                try:
                    conn.send(f"[PM] {sender_name}: {message}".encode())
                except:
                    pass
                break
                    
def send_user_list():
    users = ",".join(clients.values())
    broadcast(f"USERLIST:{users}".encode())

def handle_client(conn, addr):
    try:
        conn.send(b"NICK")
        nickname = conn.recv(1024).decode().strip()

        with lock:
            clients[conn] = nickname
        send_user_list()

        print(f"[JOIN] {nickname} from {addr}")
        broadcast(f"[SERVER] {nickname} joined\n".encode())

        while True:
            msg = conn.recv(1024)
            if not msg:
                break

            text = msg.decode()

            # private message format: @target|message
            if text.startswith("@"):
                try:
                    target, body = text[1:].split("|", 1)
                    send_private(nickname, target, body)
                except:
                    pass
            else:
                broadcast(f"{nickname}: ".encode() + msg, conn)

    except:
        pass
    finally:
        remove_client(conn)

def remove_client(conn):
    with lock:
        if conn in clients:
            nickname = clients[conn]
            del clients[conn]
            send_user_list()
            print(f"[LEAVE] {nickname}")
            broadcast(f"[SERVER] {nickname} left\n".encode())
            conn.close()

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[RUNNING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start()