import cv2
import socket
import pickle
import math
import time

# server setup
server_ip = "127.0.0.1"
server_port = 9999

# video setup
video_path = ""   # put your video path here
frame_size = (640, 360)
chunk_size = 60000
frame_delay = 0.03   # 30 fps approx

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Could not open video")
    exit()

print("[SERVER] Started streaming...")

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("[SERVER] video finished")
        break

    # resize frame
    frame = cv2.resize(frame, frame_size)

    # encode frame
    ok, buf = cv2.imencode(".jpg", frame)
    if not ok:
        print("[SERVER] error encoding frame, skipping")
        continue

    data = pickle.dumps(buf)

    # split into chunks
    total = math.ceil(len(data) / chunk_size)
    for i in range(total):
        start = i * chunk_size
        end = start + chunk_size
        chunk = data[start:end]

        marker = 1 if i == total - 1 else 0
        pkt = pickle.dumps((marker, chunk))

        try:
            sock.sendto(pkt, (server_ip, server_port))
        except:
            print("[SERVER] send error")
            break

    frame_count += 1
    if frame_count % 10 == 0:
        print("[SERVER] sent", frame_count, "frames")

    # press q to quit early
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    time.sleep(frame_delay)

cap.release()
sock.close()
print("[SERVER] Done.")
