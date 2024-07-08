import threading
import requests
import time
import os

if not os.path.exists(f"{os.path.dirname(__file__)}/images"):
    os.mkdir(f"{os.path.dirname(__file__)}/images")

index = len(os.listdir(f"{os.path.dirname(__file__)}/images"))

pause_time = 20
stop = False
thread_count = 0
max_threads = 10
queue = []

print("Starting from index", index)

def download(image_number):
    global thread_count
    global stop
    downloaded = False
    while not downloaded:
        try:
            r = requests.get(f"https://filebrowser.tumppi066.fi/api/public/dl/Uw850Xow/{image_number}.png?inline=true")
            if r.status_code == 404:
                stop = True
            queue.append([image_number, r.content])
            downloaded = True
        except:
            pass
    thread_count -= 1

for i in range(index):
    if not os.path.exists(f"{os.path.dirname(__file__)}/images/{i}.png"):
        while True:
            print(f"Downloading {i}.png as it was missing")
            if thread_count < max_threads:
                threading.Thread(target=download, args=(index,), daemon=True).start()
                thread_count += 1
                break
            else:
                time.sleep(0.02)

def WritingThread():
    global queue
    while True:
        if len(queue) > 0:
            for thing in queue:
                try:
                    with open(os.path.join(os.path.dirname(__file__), "images", f"{thing[0]}.png"), "wb") as f:
                        f.write(thing[1])
                except:
                    print(f"Failed to write {thing[0]}")

threading.Thread(target=WritingThread, daemon=True).start()
while True:
    while stop == False:
        if thread_count < max_threads:
            threading.Thread(target=download, args=(index,), daemon=True).start()
            thread_count += 1
            index += 1
        else:
            time.sleep(0.01)
        print(f"\rDownloaded {index} images                           ", end="")
    pause_start = time.time()
    while time.time() - pause_start < pause_time:
        print(f"\rWaiting for more data at {index} images ({round(pause_time - (time.time() - pause_start), 2)}s)", end="")
    stop = False
