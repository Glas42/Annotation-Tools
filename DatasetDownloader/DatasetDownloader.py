import threading
import requests
import time
import os

print("Information: This script is only meant to download datasets from filebrowser.tumppi066.fi/[Drive ID]\n")

drive_id = None
while drive_id == None:
    drive_id = input("From which drive do you want to download? (1: buYoYXfn 2: Uw850Xow)\n-> ")
    try:
        drive_id = "buYoYXfn" if drive_id == "1" else "Uw850Xow" if drive_id == "2" else None
    except:
        drive_id = None

thread_count = 0
max_threads = -1
while max_threads < 0:
    max_threads = input("How many threads do you want to use for downloading?\n-> ")
    try:
        max_threads = int(max_threads)
    except:
        max_threads = -1

print()

if not os.path.exists(f"{os.path.dirname(__file__)}/Dataset"):
    os.mkdir(f"{os.path.dirname(__file__)}/Dataset")

index = len([f for f in os.listdir(f"{os.path.dirname(__file__)}/Dataset") if f.endswith('.png')])

print("Starting from index", index)

def download(image_number):
    global thread_count
    downloaded = False
    while not downloaded:
        try:
            response = requests.get(f"https://filebrowser.tumppi066.fi/api/public/dl/{drive_id}/{image_number}.png?inline=true")
            if response.status_code == 404:
                for i in range(10):
                    if requests.get(f"https://filebrowser.tumppi066.fi/api/public/dl/{drive_id}/{image_number + i + 1}.png?inline=true").status_code != 404:
                        downloaded = True
                        break
                if downloaded:
                    break
                time.sleep(60)
                continue
            with open(f"{os.path.dirname(__file__)}/Dataset/{image_number}.png", "wb") as f:
                f.write(response.content)
            try:
                response = requests.get(f"https://filebrowser.tumppi066.fi/api/public/dl/{drive_id}/{image_number}.txt?inline=true")
                with open(f"{os.path.dirname(__file__)}/Dataset/{image_number}.txt", "wb") as f:
                    f.write(response.content)
            except:
                pass
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