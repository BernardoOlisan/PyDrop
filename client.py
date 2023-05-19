import socket
import tqdm
import os
import subprocess 
import re 

SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 4096

# this function will return ipv4 address of the machine
def get_ip() -> str:

    command_output = subprocess.run(['ipconfig'], check=True, capture_output=True, text=True).stdout
    ip_adress = re.findall(r"IPv4. . . . . . . . . . . . . . : (\d+\.\d+\.\d+\.\d+)", command_output)[0]
    return ip_adress

s = socket.socket()
host = get_ip()
port = 5001
print(f'[+] Conneting to {host}:{port}')
s.connect((host, port))
print('[+] Connected to ', host)

filename = input("File to Transfer : ")
filesize = os.path.getsize(filename)
s.send(f'{filename}{SEPARATOR}{filesize}'.encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
     
s.close()