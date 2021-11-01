import socket
import os
import tqdm

SERVER_HOST = '0.0.0.0' # All ipv4 
SERVER_PORT = 5001 # port
BUFFER_SIZE = 4096
SEPARATOR = '<SEPARATOR>'

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(10) # Connections to accept, 10 is the limit, only 10 ppl

print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT}')
print("Waiting for the client to connect...")

client_socket, address = s.accept()
hostname = socket.gethostname()
name = socket.gethostbyname(hostname)
print(f'[+] {hostname} | {address} is connected.')

received = client_socket.recv(BUFFER_SIZE).decode()

filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)


progress = tqdm.tqdm(range(filesize), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024)

with open(filename, 'wb') as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
s.close()
