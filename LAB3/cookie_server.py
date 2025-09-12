import socket
import datetime
import random

HOST = '127.0.0.1'
PORT = 8081
visitor_count = 1  # counter for assigning new user IDs

def build_response(user_cookie=None):
    global visitor_count

    if user_cookie is None:
        # frst-time visitor - assign a new cookie
        user_id = f"Guest{random.randint(1000,11000)}"
        visitor_count += 1
        message = f"<h1>Hello {user_id}, welcome for the first time!</h1>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(message)}\r\n"
            "Content-Type: text/html\r\n"
            f"Set-Cookie: session={user_id}; HttpOnly\r\n"
            "\r\n"
            f"{message}"
        )
    else:
        # returning visitor -  message
        message = f"<h1>Welcome back, {user_cookie}!</h1>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(message)}\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            f"{message}"
        )
    return response

# raw socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Cookie server running on http://{HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with conn:
            request_data = conn.recv(1024).decode('utf-8')
            if not request_data:
                continue

            # extract cookie header if present
            cookie_value = None
            for line in request_data.split("\r\n"):
                if line.startswith("Cookie:"):
                    parts = line.split(";")
                    for part in parts:
                        if "session=" in part:
                            cookie_value = part.split("=")[1].strip()
                            break

            # send response
            conn.sendall(build_response(cookie_value).encode('utf-8'))
