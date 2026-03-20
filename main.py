import openai
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import requests
import json
import time
import threading
import ctypes  # Added for built-in hardware access
import screen_brightness_control as sbc
import pythoncom
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import wintypes

# --- WINDOWS POWER STATUS STRUCTURE ---
class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]

MEMORY_FILE = "memory.json"

# --- MEMORY FUNCTIONS ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def recall(key):
    memory = load_memory()
    return memory.get(key, None)

def change_volume_by_step(step):
    """Increase or decrease volume by a relative amount (e.g. 10 or -10)"""
    try:
        # 1. Always initialize COM for background threads
        pythoncom.CoInitialize()
        
        # 2. Get the default speaker device
        devices = AudioUtilities.GetSpeakers()
        
        # 3. FIX: Access the EndpointVolume directly through the device interface
        # This bypasses the 'Activate' error seen on many Windows 10/11 systems
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # 4. Get and change volume
        current_vol = volume.GetMasterVolumeLevelScalar()
        new_vol = min(1.0, max(0.0, current_vol + (step / 100)))
        
        volume.SetMasterVolumeLevelScalar(new_vol, None)
        
        # 5. Clean up
        pythoncom.CoUninitialize()
        print(f"DEBUG: Volume is now at {int(new_vol * 100)}%")
        
    except Exception as e:
        print(f"Detailed Volume Error: {e}")

def set_brightness(level):
    """Adjusts screen brightness. level is 0 to 100"""
    sbc.set_brightness(level)


# --- CONFIGURATION ---
with open("key.txt", "r") as f:
    openai.api_key = f.read().strip()

# --- THREAD-SAFE SPEECH ---
def speak(text):
    print("Jarvis:", text)
    def _run_speech():
        try:
            # Initialize a FRESH engine instance for this specific message
            temp_engine = pyttsx3.init()
            temp_engine.setProperty("rate", 170)
            temp_engine.say(text)
            temp_engine.runAndWait() # Blocks ONLY this background thread
            
            # Clean up the engine immediately after speaking
            del temp_engine 
        except Exception as e:
            print("Speech Error:", e)
    
    # Run as a daemon thread so it doesn't block the main program from closing
    threading.Thread(target=_run_speech, daemon=True).start()
# --- HARDWARE STATUS (NO PSUTIL) ---
def get_system_condition():
    status = SYSTEM_POWER_STATUS()
    # Call Windows API directly
    if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
        percent = status.BatteryLifePercent
        # ACLineStatus: 1 = Plugged in, 0 = Unplugged
        plugged = "plugged in" if status.ACLineStatus == 1 else "unplugged"
        
        if percent == 255: # Windows returns 255 if battery not found
             return "Sir, I couldn't detect a battery on this system."
        
        return f"Sir, the battery is at {percent} percent and is currently {plugged}."
    else:
        return "I am sorry sir, I couldn't retrieve the system status."

# --- COMMANDS ---
import time # Ensure you have this import at the top

import time # Ensure this is at the top of main.py

import time # Ensure this is at the very top of your main.py

import time

import os
import time
import webbrowser

def execute_local_commands(cmd):
    cmd = cmd.lower()

    # --- 1. SEARCH LOGIC (Google, YouTube, Amazon) ---
    if any(site in cmd for site in ["google", "youtube", "amazon"]):
        target = "google" if "google" in cmd else ("youtube" if "youtube" in cmd else "amazon")
        speak(f"Opening {target}. What should I search for, sir?")
        
        time.sleep(2.5) # Wait for Jarvis to finish speaking
        
        print(f"DEBUG: Jarvis is now listening for your {target} query...")
        query = listen()
        
        if query and len(query) > 2:
            if target == "youtube":
                url = f"https://www.youtube.com/results?search_query={query}"
            elif target == "amazon":
                url = f"https://www.amazon.com/s?k={query}"
            else:
                url = f"https://www.google.com/search?q={query}"
            
            speak(f"Searching for {query} on {target}.")
            time.sleep(1.0) 
            
            try:
                webbrowser.open_new_tab(url) 
                time.sleep(1.5) 
            except Exception as e:
                print(f"Browser Error: {e}")
            return True
        else:
            speak("I didn't hear a search term, sir. Operation cancelled.")
            return True

    # --- 2. SYSTEM APPLICATIONS ---
    
    # Notepad
    if "open notepad" in cmd:
        speak("Opening Notepad, sir.")
        os.system("start notepad")
        return True

    # Calculator
    if "open calculator" in cmd:
        speak("Launching Calculator, sir.")
        os.system("start calc")
        return True

    # VLC Media Player (Assumes it is in your System Path)
    if "open vlc" in cmd:
        speak("Opening VLC Media Player, sir.")
        os.system("start vlc") # If this fails, use the full path to vlc.exe
        return True

    # This PC (File Explorer)
    if "open this pc" in cmd or "open my computer" in cmd:
        speak("Opening This PC, sir.")
        # Shell command for "This PC"
        os.system("start explorer shell:MyComputerFolder")
        return True

    # Recycle Bin
    if "open recycle bin" in cmd:
        speak("Opening the Recycle Bin, sir.")
        # Shell command for Recycle Bin
        os.system("start explorer shell:RecycleBinFolder")
        return True
    # --- VOLUME CONTROL ---
    if "volume" in cmd:
        if "increase" in cmd or "up" in cmd:
            speak("Increasing volume, sir.")
            change_volume_by_step(10) # Goes up by 10%
            return True
        elif "decrease" in cmd or "down" in cmd:
            speak("Decreasing volume, sir.")
            change_volume_by_step(-10) # Goes down by 10%
            return True
        elif "mute" in cmd:
            speak("Muting audio, sir.")
            # We can still use set_volume(0) here if you kept it, 
            # or just change_volume_by_step(-100)
            change_volume_by_step(-100) 
            return True

    if "brightness" in cmd:
        if "increase" in cmd or "up" in cmd:
            speak("Display brightened.")
            set_brightness(90)
        return True

    # --- 2. System Apps (Only one copy needed!) ---
    apps = {
        "notepad": "start notepad",
        "calculator": "start calc",
        "vlc": "start vlc",
        "this pc": "start explorer shell:MyComputerFolder"
    }
    
    for app_name, app_cmd in apps.items():
        if f"open {app_name}" in cmd:
            speak(f"Opening {app_name}, sir.")
            os.system(app_cmd)
            return True

    # --- BRIGHTNESS CONTROL ---
    if "brightness" in cmd:
        if "increase" in cmd or "up" in cmd:
            speak("Brightening the display.")
            set_brightness(100)
        elif "decrease" in cmd or "down" in cmd:
            speak("Dimming the display.")
            set_brightness(10)
        return True
   
    return False

# --- CORE LOGIC ---
    
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # This helps ignore background noise
        r.adjust_for_ambient_noise(source, duration=0.5) 
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            return r.recognize_google(audio, language="en-in").lower()
        except:
            return ""

def ask_gpt(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a formal British AI."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except:
        return "I am having trouble accessing my brain right now, sir."

# --- MAIN LOOP ---
if __name__ == "__main__":
    speak("System online. How can I assist you?")
    while True:
        command = listen()
        if not command: continue

        if any(word in command for word in ["stop", "shutdown", "goodbye"]):
            speak("Shutting down. Goodbye!")
            break

        if execute_local_commands(command):
            continue

        # AI Fallback
        speak(ask_gpt(command))
