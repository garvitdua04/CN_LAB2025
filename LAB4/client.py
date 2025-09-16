import cv2
import socket
import pickle

# Client settings
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 9999

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((CLIENT_IP, CLIENT_PORT))

    buffer = []
    print("[CLIENT] Waiting for video stream...")

    try:
        while True:
            try:
                packet, _ = sock.recvfrom(65536)  # receive packet
                marker, chunk = pickle.loads(packet)  # (marker, chunk)

                buffer.append(chunk)

                if marker == 1:  # last chunk of frame
                    data = b"".join(buffer)
                    buffer.clear()

                    try:
                        frame_data = pickle.loads(data)
                        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

                        if frame is not None:
                            cv2.imshow("UDP Video Stream", frame)

                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            break
                    except Exception as e:
                        print(f"[CLIENT] Frame decode error: {e}")

            except Exception as e:
                print(f"[CLIENT] Packet error: {e}")

    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user")

    finally:
        sock.close()
        cv2.destroyAllWindows()
        print("[CLIENT] Streaming finished")

if __name__ == "__main__":
    main()
