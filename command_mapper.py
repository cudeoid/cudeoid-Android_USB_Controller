import os
import xml.etree.ElementTree as ET
import re
from ocr_fallback import find_text_coordinates_ocr
import difflib

def adb_shell(command):
    os.system(f"adb shell {command}")

def get_xml_ui():
    os.system("adb shell uiautomator dump /sdcard/ui.xml")
    os.system("adb pull /sdcard/ui.xml")
    return "ui.xml"


def best_match_action(unknown_text, known_actions):
    matches = difflib.get_close_matches(unknown_text, known_actions, n=1, cutoff=0.5)
    return matches[0] if matches else None

# def find_text_coordinates_xml(target):
#     xml_file = get_xml_ui()
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#     matches = []
#     for node in root.iter("node"):
#         if target.lower() in node.attrib.get("text", "").lower():
#             bounds = node.attrib.get("bounds")
#             matches.append(bounds)
#     if not matches:
#         return None
#     x1, y1, x2, y2 = map(int, matches[0].strip("[]").replace("] [", ",").split(","))
#     return ((x1 + x2) // 2, (y1 + y2) // 2)



def find_text_coordinates_xml(target):
    xml_file = get_xml_ui()
    tree = ET.parse(xml_file)
    root = tree.getroot()
    matches = []
    for node in root.iter("node"):
        if target.lower() in node.attrib.get("text", "").lower():
            bounds = node.attrib.get("bounds")
            matches.append(bounds)
    if not matches:
        return None

    # Use regex to extract all 4 numbers from the bounds string
    bounds = matches[0]  # e.g., "[0,336][1080,531]"
    numbers = list(map(int, re.findall(r'\d+', bounds)))
    x1, y1, x2, y2 = numbers
    return ((x1 + x2) // 2, (y1 + y2) // 2)


def handle_command(command):
    action = command.get("action")
    print(action)
    if action == "scroll":
        direction = command.get("direction", "")
        if direction == "down":
            adb_shell("input swipe 500 1500 500 300")
        elif direction == "up":
            adb_shell("input swipe 500 300 500 1500")

    elif action == "swipe":
        direction = command.get("direction", "")
        if direction == "left":
            adb_shell("input swipe 1000 800 100 800")
        elif direction == "right":
            adb_shell("input swipe 100 800 1000 800")

    elif action == "click":
        target = command.get("target", "")
        coords = find_text_coordinates_xml(target)
        if coords is None:
            coords = find_text_coordinates_ocr(target)
        if coords:
            adb_shell(f"input tap {coords[0]} {coords[1]}")
        else:
            print("Target not found.")

    elif action == "type":
        text = command.get("text", "").replace(" ", "%s")
        adb_shell(f"input text {text}")

    elif action == "back":
        adb_shell("input keyevent 4")

    elif action == "home":
        adb_shell("input keyevent 3")

    elif action == "lock":
        adb_shell("input keyevent 26")

    elif action == "unlock":
        adb_shell("input keyevent 26")
        adb_shell("input swipe 500 1200 500 400")

    else:
        print(f"Unknown action: '{command.get('text')}'")
        suggestion = best_match_action(command.get("text", ""), ["scroll", "swipe", "click", "type", "back", "home", "lock", "unlock"])
        if suggestion:
            print(f"Did you mean: '{suggestion}'? Executing as '{suggestion}'.")
            command["action"] = suggestion
            handle_command(command)
        else:
            print("No similar action found. Command skipped.")

    # else:
    #     print("Unrecognized command.")