import cv2
import pyautogui
import numpy as np
import socket
import pickle
import struct
import threading

# Function to capture the screen
def capture_screen():
    # Capture the screen using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to an OpenCV compatible format
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame

# Function to handle window display
def display_window():
    # Create a window to display the captured screen
    cv2.namedWindow('Screen Capture', cv2.WINDOW_NORMAL)
    while True:
        try:
            # Capture the screen
            frame = capture_screen()

            # Display the captured screen
            cv2.imshow('Screen Capture', frame)

            # Check for user input or if the window is closed
            key = cv2.waitKey(1)
            if key == ord('q') or key == 27 or cv2.getWindowProperty('Screen Capture', cv2.WND_PROP_VISIBLE) < 1:
                break

        except Exception as e:
            print(f"Error: {e}")
            break
    cv2.destroyAllWindows()

# Function to send frame over socket connection
def send_frame(client_socket, frame):
    # Serialize the frame
    data = pickle.dumps(frame)

    # Pack the frame size
    message_size = struct.pack("L", len(data))

    # Send the message size
    client_socket.sendall(message_size)

    # Send the serialized frame
    client_socket.sendall(data)

# Function to handle client connection
def handle_client(client_socket, addr):
    print(f"Connection established with {addr}")

    while True:
        try:
            # Capture the screen
            frame = capture_screen()

            # Send the frame over the socket connection
            send_frame(client_socket, frame)

        except Exception as e:
            print(f"Error: {e}")
            break

    # Release the client socket
    client_socket.close()

# Main function
def main():
    # Start window display thread
    display_thread = threading.Thread(target=display_window)
    display_thread.start()

    # Start streaming server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 6969))
    server_socket.listen(5)
    print("Streaming server started. Waiting for connections...")

    while True:
        # Accept connection from client
        client_socket, addr = server_socket.accept()

        # Handle client connection in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

    # Release the server socket
    server_socket.close()

if __name__ == "__main__":
    main()