import cv2
import pyautogui
import pyaudio
import socket
import numpy as np
import zlib
import signal
import sys

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Define constants
SCREEN_RESOLUTION = (1920, 1080)  # Example screen resolution
AUDIO_SAMPLE_RATE = 44100  # Example audio sample rate
AUDIO_CHUNK_SIZE = 1024  # Example audio chunk size
SERVER_IP = '0.0.0.0'  # Bind to all available network interfaces
SERVER_PORT = 8888  # Example server port

# Global variable to track whether the server is running
server_running = True

# Function to capture screen frames
def capture_screen():
    screen = pyautogui.screenshot()
    frame = np.array(screen)
    return frame

# Function to capture audio
def capture_audio():
    format = pyaudio.paInt16  # 16-bit resolution
    channels = 1  # Mono

    stream = audio.open(format=format,
                        channels=channels,
                        rate=AUDIO_SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=AUDIO_CHUNK_SIZE)

    frames = []
    while server_running:
        data = stream.read(AUDIO_CHUNK_SIZE)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    audio_data = b''.join(frames)

    return audio_data

# Function to encode screen frame
def encode_screen_frame(screen_frame):
    _, buffer = cv2.imencode('.jpg', screen_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return buffer

# Function to encode audio data
def encode_audio_data(audio_data):
    compressed_audio_data = zlib.compress(audio_data)
    return compressed_audio_data

# Function to send encoded data to the client
def send_data_to_client(encoded_screen_frame, encoded_audio_data, client_socket):
    client_socket.sendall(encoded_screen_frame)
    client_socket.sendall(encoded_audio_data)

# Function to receive commands from the client
def receive_commands_from_client(client_socket):
    return client_socket.recv(1024)  

# Placeholder function to process commands
def process_commands(command):
    print("Received command:", command)

# Signal handler to handle termination signal
def signal_handler(sig, frame):
    global server_running
    print("Closing server...")
    server_running = False

# Main function
def main():
    global server_running
    # Register signal handler for termination signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)

    print("Server is listening...")

    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)

    while server_running:
        screen_frame = capture_screen()
        audio_data = capture_audio()

        encoded_screen_frame = encode_screen_frame(screen_frame)
        encoded_audio_data = encode_audio_data(audio_data)

        send_data_to_client(encoded_screen_frame, encoded_audio_data, client_socket)

        command = receive_commands_from_client(client_socket)
        process_commands(command)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
