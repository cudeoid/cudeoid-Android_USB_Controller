import cv2
import pytesseract
import numpy as np
import os

def screenshot():
    os.system("adb exec-out screencap -p > screen.png")

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return blur

def find_text_coordinates_ocr(target):
    screenshot()
    img = cv2.imread("screen.png")
    processed = preprocess_image(img)
    data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
    matches = []
    for i in range(len(data['text'])):
        if target.lower() in data['text'][i].lower():
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            matches.append((x, y))
    if not matches:
        return None
    if len(matches) > 1:
        print("Multiple matches found:")
        for i, (x, y) in enumerate(matches):
            print(f"{i+1}: {target} at ({x},{y})")
        choice = int(input("Choose option: ")) - 1
        return matches[choice]
    return matches[0]