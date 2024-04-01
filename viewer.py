import cv2
import numpy as np
import socket
import tkinter as tk
from PIL import Image, ImageTk

# Client parameters
server_ip = '127.0.0.1'  # Change this to the server's IP address
server_port = 12345  # Change this to the server's port

# Function to receive and display frames
def receive_and_display():
    print("Starting receive_and_display function...")

    # Create Tkinter window
    root = tk.Tk()
    root.title("UDP Image Viewer")
    
    # Create label to display images
    label = tk.Label(root)
    label.pack()
    
    # Function to update image in label
    def update_image(frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        label.config(image=image)
        label.image = image
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_ip, server_port))

    print("Socket created and bound. Starting loop...")
    
    # Continuously receive and display images
    while True:
        # Receive data from the server
        data, _ = sock.recvfrom(65507)  # Adjust buffer size as needed
        
        # Decode the received JPEG data to image
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Display the received frame
        update_image(frame)
        
        # Update the Tkinter window
        root.update_idletasks()
        root.update()

    # Close the Tkinter window
    root.mainloop()

# Main function
def main():
    receive_and_display()

if __name__ == "__main__":
    main()
