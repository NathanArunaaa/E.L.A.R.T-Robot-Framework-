import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Raspberry Pi's IP address and port
host = 'RASPBERRY_PI_IP_ADDRESS'  # Replace with the Raspberry Pi's IP address on the access point network
port = 12345                      # Use the same port number chosen on the Raspberry Pi
client_socket.connect((host, port))

while True:
    command = input("Enter a command: ")
    client_socket.send(command.encode())
    if command.lower() == 'exit':
        break

client_socket.close()