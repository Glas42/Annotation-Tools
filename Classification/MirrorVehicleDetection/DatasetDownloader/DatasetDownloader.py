import threading
import requests
import time
import os

if not os.path.exists(f"{os.path.dirname(__file__)}/Dataset"):
    os.mkdir(f"{os.path.dirname(__file__)}/Dataset")

index = len(os.listdir(f"{os.path.dirname(__file__)}/Dataset"))

thread_count = 0
max_threads = 100

print("Starting from index", index)

def download(image_number):
    global thread_count
    downloaded = False
    while not downloaded:
        try:
            r = requests.get(f"https://filebrowser.tumppi066.fi/api/public/dl/Uw850Xow/{image_number}.png?inline=true")
            if r.status_code == 404:
                time.sleep(60)
                continue
            with open(f"{os.path.dirname(__file__)}/Dataset/{image_number}.png", "wb") as f:
                f.write(r.content)
            downloaded = True
        except:
            time.sleep(60)
    thread_count -= 1

for i in range(index):
    if not os.path.exists(f"{os.path.dirname(__file__)}/Dataset/{i}.png"):
        print(f"\rDownloading {i} because the previous download did not download it...", end="")
        while True:
            if thread_count < max_threads:
                threading.Thread(target=download, args=(index,), daemon=True).start()
                thread_count += 1
                break
            else:
                time.sleep(0.01)

print(f"\r                                                                                           ", end="")

while True:
    if thread_count < max_threads:
        threading.Thread(target=download, args=(index,), daemon=True).start()
        thread_count += 1
        index += 1
        print(f"\rDownloaded {index} files", end="")
    else:
        time.sleep(0.01)