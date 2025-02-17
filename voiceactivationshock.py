import random
import json
import os
import speech_recognition as sr 
import requests
import time
import traceback
import sys
print(sys.executable)

CONFIG_FILE = "config.json"  # File to store user details

def load_config():
    """Load API details from config file if it exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}  # Return empty if file does not exist

def save_config(config):
    """Save API details to a config file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    print("✅ Configuration saved!")

def reset_config():
    """Delete the config file to reset settings."""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("🔄 Configuration reset! You will need to enter new details.")
    else:
        print("⚠️ No existing configuration found.")

def get_user_details():
    """Ask the user for details only if not already saved."""
    config = load_config()

    if config and input("🔄 Do you want to reset your settings? (yes/no): ").strip().lower() in ["yes", "y"]:
        reset_config()
        config = {}  # Clear config to force re-entry

# Ask for details if not already saved
    if "API_KEY" not in config:
        config["API_KEY"] = input("Enter your PiShock API Key: ").strip()
    if "USERNAME" not in config:
        config["USERNAME"] = input("Enter your PiShock Username: ").strip()
    if "DEVICE_ID" not in config:
        config["DEVICE_ID"] = input("Enter your PiShock code (not link): ").strip()

    save_config(config)  # Save details for next time
    return config

# Load or prompt for API details
user_config = get_user_details()

# Use the stored details
API_KEY = user_config["API_KEY"]
USERNAME = user_config["USERNAME"]
DEVICE_ID = user_config["DEVICE_ID"]

print(f"🔗 Using API Key: {API_KEY}")
print(f"👤 Username: {USERNAME}")
print(f"📡 Device ID: {DEVICE_ID}")

# PiShock API details
# API_KEY = input("Enter your PiShock API Key: ").strip()
# USERNAME = input("Enter your PiShock Username: ").strip()
# DEVICE_ID = input("Enter your PiShock code (not link): ").strip()
# INTENSITY = random.randint(1, 35)  # Adjust intensity (1-100)
# DURATION = random.randint(1, 7)  # Shock duration in seconds

print("!!!The shocks will be random strength and duration. be sure you set limits in the link!!!")

# Different sets of curse words with labeled categories
TRIGGER_WORD_LISTS = {
    1: ("standard list", [
      "damn", "damnit", "hell", "shit", "fuck", "fucks", "fucker", "bitch", "bich", "asshole", 
      "niger", "nigga", "cunt", "dick", "faggot", "kill yourself", "KYS", "midget", "pussy", 
      "kkk", "Ku Klux Klan","fucking", "fuckin'", "fuk", "fuc", "ass", "whore","freaking",
      "dammit",
      ]),
}


TRIGGER_WORDS = random.choice(list(TRIGGER_WORD_LISTS.values()))[1]  # Picks a random category



def send_shock():
    """Sends a shock command to PiShock."""
    INTENSITY = random.randint(1, 100)  # Adjust intensity (1-100)
    DURATION = random.randint(1, 15)  # Shock duration in seconds
    url = "https://do.pishock.com/api/apioperate"
    data = {
    "Username": USERNAME,  # Your PiShock username
    "Apikey": API_KEY,     # Your PiShock API key
    "Op": "0",                         # "0" = Shock, "1" = Vibrate, "2" = Beep
    "Intensity": INTENSITY,                  # Intensity (1-100)
    "Duration": DURATION,                     # Duration in seconds (1-15)
    "Code": DEVICE_ID     # Your PiShock device code
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("⚡ Shock sent! Watch your language! ⚡")
    else:
        print(f"❌ Failed to send shock: {response.json()}")

def listen_and_detect():
    """Continuously listens for speech and checks for curse words."""
    recognizer = sr.Recognizer()
    
    # mic_index = 2  # Change this to match your mic from list_microphone_names()
    # mic_index = 2 is hyperX headset
    # mic_index = 1 or 8 is VRset headset
    # 7 2 12 23 are all PC mics
    



    with sr.Microphone() as source:
        print(f"🎤 Using default microphone: {sr.Microphone.list_microphone_names()[0]}")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                print("⏳ Waiting for speech...")
                audio = recognizer.listen(source, phrase_time_limit=3)
                text = recognizer.recognize_google(audio, language="en-US").lower()
                print(f"🗣 You said: {text}")

                # Check for curse words
                if any(word in text for word in TRIGGER_WORDS):
                    print("🚨 Curse word detected!")
                    send_shock()
                    time.sleep(2)  # Prevent rapid shocks

            except sr.UnknownValueError:
                print("🤔 Couldn't understand, try again.")
            except sr.RequestError as e:
                print(f"⚠️ Error with speech recognition: {e}")
            except Exception as e:
               print(f"An error occurred: {e}")  # Shows the error
               input("Press Enter to try again...")

if __name__ == "__main__":
    listen_and_detect()