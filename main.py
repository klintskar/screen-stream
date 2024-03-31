import tkinter as tk
import os

def launch_server_gui():
    os.system("python server.py")

def launch_client_gui():
    root.destroy()
    client_type_window = tk.Tk()
    client_type_window.title("Choose Client Type")
    client_type_window.geometry("200x150")
    client_type_window.configure(bg="blue")  # Server UI color

    def stream(server_ip):
        client_type_window.destroy()
        os.system(f"python client.py --stream {server_ip}")

    def view(server_ip):
        client_type_window.destroy()
        os.system(f"python client.py --view {server_ip}")

    def start_stream():
        server_ip = server_ip_entry.get()
        stream(server_ip)

    def start_view():
        server_ip = server_ip_entry.get()
        view(server_ip)

    server_ip_label = tk.Label(client_type_window, text="Server IP:")
    server_ip_label.pack(pady=5)

    server_ip_entry = tk.Entry(client_type_window)
    server_ip_entry.pack(pady=5)

    stream_button = tk.Button(client_type_window, text="Stream", command=start_stream, bg="red")  # Stream button color
    stream_button.pack(pady=10)

    view_button = tk.Button(client_type_window, text="View", command=start_view, bg="blue")  # View button color
    view_button.pack(pady=10)

    client_type_window.mainloop()

root = tk.Tk()
root.title("Streaming Application")
root.geometry("200x200")
root.configure(bg="green")  # Client UI color

server_button = tk.Button(root, text="Start Server", command=launch_server_gui, bg="blue")  # Server button color
server_button.pack(pady=10)

client_button = tk.Button(root, text="Start Client", command=launch_client_gui, bg="green")  # Client button color
client_button.pack(pady=10)

root.mainloop()
