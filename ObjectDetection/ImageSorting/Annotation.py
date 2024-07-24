import numpy as np
import keyboard
import datetime
import shutil
import ctypes
import mouse
import time
import cv2
import os


#     class name ↓           ↓ keyboard key to select the class      ↓ is the button a radio button
CLASSES = []

Continue_Key = "a"
Delete_Key = "s"

PATH = os.path.join(os.path.dirname(__file__), "DatasetAssets", "NotDetected")
UNANNOTED_IMAGES_PATH = os.path.join(os.path.dirname(__file__), "DatasetAssets", "UnannotatedImages")
window_name = "Annotiation"
frame_width = 1800
frame_height = 600

images = []
selected_classes = []
last_pressed_keys = []
last_left_clicked = False
last_window_size = frame_width, frame_height
load_from_disk = True
max_image_limit = 1000

def get_text_size(text="NONE", text_width=0.5*frame_width, max_text_height=0.5*frame_height):
    fontscale = 1
    textsize, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontscale, 1)
    width_current_text, height_current_text = textsize
    max_count_current_text = 3
    while width_current_text != text_width or height_current_text > max_text_height:
        fontscale *= min(text_width / textsize[0], max_text_height / textsize[1])
        textsize, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontscale, 1)
        max_count_current_text -= 1
        if max_count_current_text <= 0:
            break
    thickness = round(fontscale * 2)
    if thickness <= 0:
        thickness = 1
    return text, fontscale, thickness, textsize[0], textsize[1]


def make_button(text="NONE", x1=0, y1=0, x2=100, y2=100, round_corners=30, buttoncolor=(100, 100, 100), buttonhovercolor=(130, 130, 130), buttonselectedcolor=(160, 160, 160), buttonselected=False, textcolor=(255, 255, 255), width_scale=0.9, height_scale=0.8):
    if x1 <= mouse_x*frame_width <= x2 and y1 <= mouse_y*frame_height <= y2:
        buttonhovered = True
    else:
        buttonhovered = False
    if buttonselected == True:
        cv2.rectangle(frame, (round(x1+round_corners/2), round(y1+round_corners/2)), (round(x2-round_corners/2), round(y2-round_corners/2)), buttonselectedcolor, round_corners)
        cv2.rectangle(frame, (round(x1+round_corners/2), round(y1+round_corners/2)), (round(x2-round_corners/2), round(y2-round_corners/2)), buttonselectedcolor, -1)
    elif buttonhovered == True:
        cv2.rectangle(frame, (round(x1+round_corners/2), round(y1+round_corners/2)), (round(x2-round_corners/2), round(y2-round_corners/2)), buttonhovercolor, round_corners)
        cv2.rectangle(frame, (round(x1+round_corners/2), round(y1+round_corners/2)), (round(x2-round_corners/2), round(y2-round_corners/2)), buttonhovercolor, -1)
    else:
        cv2.rectangle(frame, (round(x1+round_corners/2), round(y1+round_corners/2)), (round(x2-round_corners/2), round(y2-round_corners/2)), buttoncolor, round_corners)
        cv2.rectangle(frame, (round(x1+round_corners/2), round(y1+round_corners/2)), (round(x2-round_corners/2), round(y2-round_corners/2)), buttoncolor, -1)
    text, fontscale, thickness, width, height = get_text_size(text, round((x2-x1)*width_scale), round((y2-y1)*height_scale))
    cv2.putText(frame, text, (round(x1 + (x2-x1) / 2 - width / 2), round(y1 + (y2-y1) / 2 + height / 2)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, textcolor, thickness, cv2.LINE_AA)
    if x1 <= mouse_x*frame_width <= x2 and y1 <= mouse_y*frame_height <= y2 and left_clicked == False and last_left_clicked == True:
        return True, buttonhovered
    else:
        return False, buttonhovered

if PATH == None or os.path.exists(PATH) == False:
    print("PATH does not exist, exiting...")
    exit()
total_images = len(os.listdir(f"{PATH}"))
print(f"Creating image list... (0/{total_images})", end="\r") 
if load_from_disk == True:
    for i, file in enumerate(os.listdir(f"{PATH}")):
        images.append([os.path.join(f"{PATH}", file), f"{file}"])
        print(f"Creating image list... ({i+1}/{total_images})", end="\r")
else:
    for i, file in enumerate(os.listdir(f"{PATH}")):
        images.append([cv2.imread(os.path.join(f"{PATH}", file)), f"{file}"])
        print(f"Creating image list... ({i+1}/{total_images})", end="\r")

print("\nCreated image list.")

print("Creating window...")
background = np.zeros((frame_height, frame_width, 3), np.uint8)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, frame_width, frame_height)
cv2.imshow(window_name, background)
cv2.waitKey(1)
if os.name == "nt":
    import win32gui
    from ctypes import windll, byref, sizeof, c_int
    hwnd = win32gui.FindWindow(None, window_name)
    windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, byref(c_int(0x000000)), sizeof(c_int))
print("Created window.")

for i, (_, key, _) in enumerate(CLASSES):
    try:
        keyboard.is_pressed(key)
    except:
        print(f'The key "{key}" is not a valid key, exiting...')
        exit()
try:
    keyboard.is_pressed(Continue_Key)
except:
    print(f'The key "{Continue_Key}" is not a valid key, exiting...')
    exit()
try:
    keyboard.is_pressed(Delete_Key)
except:
    print(f'The key "{Delete_Key}" is not a valid key, exiting...')
    exit()

total_counter = 0
annotation_counter = 0
for file in os.listdir(f"{PATH}"):
    if file.endswith(".txt") and os.path.exists(os.path.join(f"{PATH}", file.replace(".txt", ".png"))) == True:
        annotation_counter += 1
    if file.endswith(".png"):
        total_counter += 1
if total_counter > max_image_limit and max_image_limit > 0:
    total_counter = max_image_limit
print(f"\r{annotation_counter}/{total_counter} annotated...   ", end="")

index = 0
annotation_start = time.time()
while True:

    if index >= total_counter:
        print("\nAll images annotated, exiting...")
        break

    if ctypes.windll.user32.GetKeyState(0x01) & 0x8000 != 0 and ctypes.windll.user32.GetForegroundWindow() == ctypes.windll.user32.FindWindowW(None, window_name):
        left_clicked = True
    else:
        left_clicked = False

    try:
        window_x, window_y, window_width, window_height = cv2.getWindowImageRect(window_name)
        mouse_x, mouse_y = mouse.get_position()
        mouse_relative_window = mouse_x-window_x, mouse_y-window_y
        if window_width != last_window_size[0] or window_height != last_window_size[1]:
            background = np.zeros((window_height, window_width, 3), np.uint8)
        last_window_size = window_width, window_height
    except:
        exit()

    if window_width != 0 and window_height != 0:
        mouse_x = mouse_relative_window[0]/window_width
        mouse_y = mouse_relative_window[1]/window_height
    else:
        mouse_x = 0
        mouse_y = 0

    if load_from_disk:
        image_path, file = images[index]
        image = cv2.imread(image_path)
    else:
        image, file = images[index]

    frame = background.copy()
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    try:
        image_resized = cv2.resize(image, (round(frame_width * 0.93), frame_height))
        frame[0:image_resized.shape[0], 0:image_resized.shape[1]] = image_resized
    except:
        print(f"\nError resizing image: {f'{PATH}/{file}'}, skipping image...")
        index += 1

    pressed_keys = []
    current_pressed_keys = []
    for i, (_, key, _) in enumerate(CLASSES):
        if keyboard.is_pressed(key):
            current_pressed_keys.append(key)
    if keyboard.is_pressed(Continue_Key):
        current_pressed_keys.append(Continue_Key)
    if keyboard.is_pressed(Delete_Key):
        current_pressed_keys.append(Delete_Key)
    for key in current_pressed_keys:
        if key in current_pressed_keys and key not in last_pressed_keys:
            pressed_keys.append(key)

    any_radio_button_selected = False
    for i in range(len(CLASSES)):
        if CLASSES[i][2]:
            any_radio_button_selected = True if CLASSES[i][0] in selected_classes else any_radio_button_selected

    buttons = []
    for i in range(len(CLASSES) + 1):
        if i != len(CLASSES):
            button_pressed, button_hovered = make_button(text=f"{str(CLASSES[i][0]).capitalize()} (Key: {str(CLASSES[i][1]).upper()})",
                                                         x1=0.605*frame_width,
                                                         y1=((i / (len(CLASSES) + 1) + 0.01) * 0.99)*frame_height,
                                                         x2=0.995*frame_width,
                                                         y2=(((i + 1) / (len(CLASSES) + 1)) * 0.99)*frame_height,
                                                         round_corners=30,
                                                         buttoncolor=(100, 100, 100),
                                                         buttonhovercolor=(120, 120, 120),
                                                         buttonselectedcolor=(120, 180, 120),
                                                         buttonselected=True if CLASSES[i][0] in selected_classes else False,
                                                         textcolor=(255, 255, 255),
                                                         width_scale=0.95,
                                                         height_scale=0.25)
            if str(CLASSES[i][1]).lower() in pressed_keys and CLASSES[i][0] not in selected_classes and not any_radio_button_selected:
                selected_classes.append(CLASSES[i][0])
            elif str(CLASSES[i][1]).lower() in pressed_keys and CLASSES[i][0] not in selected_classes and any_radio_button_selected:
                for j in range(len(CLASSES)):
                    if CLASSES[i][2] == True and CLASSES[j][0] in selected_classes:
                        selected_classes.remove(CLASSES[j][0])
                selected_classes.append(CLASSES[i][0])
            elif str(CLASSES[i][1]).lower() in pressed_keys and CLASSES[i][0] in selected_classes:
                selected_classes.remove(CLASSES[i][0])
        else:
            button_delete_pressed, button_delete_hovered = make_button(text=f"Delete",
                                                                       x1=0.94*frame_width,
                                                                       y1=frame_height / 2 + 4,
                                                                       x2=0.990*frame_width,
                                                                       y2=frame_height - 4,
                                                                       round_corners=30,
                                                                       buttoncolor=(40, 40, 200),
                                                                       buttonhovercolor=(60, 60, 220),
                                                                       buttonselectedcolor=(60, 60, 220),
                                                                       textcolor=(255, 255, 255),
                                                                       width_scale=0.95,
                                                                       height_scale=0.3)
            button_continue_pressed, button_continue_hovered = make_button(text=f"Continue",
                                                                           x1=0.94*frame_width,
                                                                           y1=4,
                                                                           x2=0.990*frame_width,
                                                                           y2=frame_height / 2 - 4,
                                                                           round_corners=30,
                                                                           buttoncolor=(40, 200, 40),
                                                                           buttonhovercolor=(60, 220, 60),
                                                                           buttonselectedcolor=(60, 220, 60),
                                                                           textcolor=(255, 255, 255),
                                                                           width_scale=0.95,
                                                                           height_scale=0.3)
        #buttons.append((button_pressed, button_hovered))

    if button_delete_pressed:
        try:
            os.remove(f"{PATH}/{file}")
            annotation_counter += 1
        except:
            print(f"\nError deleting image: {f'{PATH}/{file}'}")
        selected_classes = []
        images.pop(index)
        index += 1      
        print(f"\r{annotation_counter}/{total_counter} annotated...   ", end="")

    for i, (button_pressed, button_hovered) in enumerate(buttons):
        if button_pressed and CLASSES[i][0] not in selected_classes and not any_radio_button_selected:
            selected_classes.append(CLASSES[i][0])
        elif button_pressed and CLASSES[i][0] not in selected_classes and any_radio_button_selected:
            for j in range(len(CLASSES)):
                if CLASSES[i][2] == True and CLASSES[j][0] in selected_classes:
                    selected_classes.remove(CLASSES[j][0])
            selected_classes.append(CLASSES[i][0])
        elif button_pressed and CLASSES[i][0] in selected_classes:
            selected_classes.remove(CLASSES[i][0])

    if button_continue_pressed:
        _, file_name = images[index]
        shutil.copyfile(f"{PATH}\{file_name}", f"{UNANNOTED_IMAGES_PATH}\{file_name}")
        os.remove(f"{PATH}/{file}")
        images.pop(index)
        annotation_counter += 1
        selected_classes = []
        index += 1
        print(f"\r{annotation_counter}/{total_counter} annotated...   ", end="")

    last_left_clicked = left_clicked
    last_pressed_keys = current_pressed_keys

    cv2.imshow(window_name, frame)
    cv2.waitKey(1)

annotation_end = time.time()
annotation_time = annotation_end - annotation_start
annotation_time_formatted = str(datetime.timedelta(seconds=annotation_time))

print(f"Annotation time: {annotation_time_formatted}")
