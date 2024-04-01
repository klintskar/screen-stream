import cv2
import socket
import pickle
import struct

# Function to receive frame from server
def receive_frame(client_socket):
    # Receive the message size
    message_size = client_socket.recv(8)

    # Unpack the message size
    message_size = struct.unpack("L", message_size)[0]

    # Receive the serialized frame
    data = b""
    while len(data) < message_size:
        packet = client_socket.recv(message_size - len(data))
        if not packet:
            return None
        data += packet

    # Deserialize the frame
    frame = pickle.loads(data)

    return frame

def main():
    # Open a window
    cv2.namedWindow('Remote Screen', cv2.WINDOW_NORMAL)

    # Get the IP address of the server
    server_ip = input("Enter the IP address of the streaming server: ")

    # Connect to the streaming server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 6969))
    print("Connected to server.")

    while True:
        try:
            # Receive frame from server
            frame = receive_frame(client_socket)

            if frame is None:
                print("Connection closed by server.")
                break

            # Display the received frame
            cv2.imshow('Remote Screen', frame)

            # Break the loop when 'q' is pressed or if the window is closed
            key = cv2.waitKey(1)
            if key == ord('q') or cv2.getWindowProperty('Remote Screen', cv2.WND_PROP_VISIBLE) < 1:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    # Release the client socket
    client_socket.close()

    # Release the window and destroy it
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
