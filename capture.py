import cv2
import numpy as np
import threading
import time
import pyautogui
import socket
import signal

# Global variable to hold the latest frame
latest_frame = None
capture_running = True
UDP_IP = "localhost"
UDP_PORT = 12345

# Function to capture the screen
def capture_screen():
    global latest_frame
    while capture_running:
        # Capture the screen using pyautogui
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to an OpenCV compatible format
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Encode frame using VP9 codec
        _, encoded_frame = cv2.imencode('.webm', frame)
        latest_frame = encoded_frame.tobytes()

        # Display the captured screen in a window
        cv2.imshow('Screen Capture', frame)

        # Check for user input or if the window is closed
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27 or cv2.getWindowProperty('Screen Capture', cv2.WND_PROP_VISIBLE) < 1:
            break

        # Sleep to control frame rate
        time.sleep(0.1)

    # Close OpenCV windows
    cv2.destroyAllWindows()

# Function to send frames over UDP
def send_frames_over_udp():
    global latest_frame
    while capture_running:
        if latest_frame is not None:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Send frame over UDP
            sock.sendto(latest_frame, (UDP_IP, UDP_PORT))

            # Close socket
            sock.close()

# Signal handler function to gracefully stop the threads
def signal_handler(sig, frame):
    global capture_running
    print("\nStopping...")
    capture_running = False

# Main function
def main():
    global capture_running
    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Start capture_screen function in a separate thread
    capture_thread = threading.Thread(target=capture_screen)
    capture_thread.start()

    # Start send_frames_over_udp function in a separate thread
    send_thread = threading.Thread(target=send_frames_over_udp)
    send_thread.start()

    # Wait for threads to finish
    capture_thread.join()
    send_thread.join()

if __name__ == "__main__":
    main()
