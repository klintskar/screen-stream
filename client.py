import cv2
import pyaudio
import socket
import numpy as np
import zlib
import sys

# Define constants
CLIENT_PORT = 8888  # Example client port
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class Client:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, CLIENT_PORT))
        print("Connected to server.")

    def send_audio(self, audio_stream):
        while True:
            data = audio_stream.read(CHUNK_SIZE)
            self.client_socket.sendall(data)

    def send_video(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            frame = cv2.resize(frame, (1920, 1080))  # Ensure the same resolution as the server
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            jpg_as_text = zlib.compress(buffer, 9)
            self.client_socket.sendall(jpg_as_text)

        cap.release()

    def receive_video(self):
        while True:
            # Receive compressed JPEG data
            jpg_as_text = self.client_socket.recv(4096)
            # Decompress JPEG data
            jpg_buffer = zlib.decompress(jpg_as_text, zlib.MAX_WBITS|32)
            # Decode JPEG data to frame
            frame = cv2.imdecode(np.frombuffer(jpg_buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
            # Display the frame
            cv2.imshow('Received Video', frame)
            # Check for 'q' key press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["--stream", "--view"]:
        print("Usage: python client.py [--stream | --view]")
        return

    client_type = sys.argv[1]

    if client_type == "--stream":
        # If streaming, the server IP can be specified as a command-line argument
        if len(sys.argv) != 3:
            print("Usage: python client.py --stream <server_ip>")
            return
        server_ip = sys.argv[2]
        client = Client(server_ip)
        client.connect()
        audio_stream = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

        client.send_audio(audio_stream)
        client.send_video()

    elif client_type == "--view":
        # If viewing, prompt the user for the server IP
        server_ip = input("Enter server IP: ")
        client = Client(server_ip)
        client.connect()
        client.receive_video()

if __name__ == "__main__":
    main()
