import os
from instagrapi import Client
import json

# List of accounts with their login credentials
accounts = [
   # {"username": "lewaset306", "password": "Admin123!", "proxy": "http://nfrvpwlvajujbee96234-zone-resi-region-us:hayfcmmpcg@resi-us.lightningproxies.net:9999"},
    {"username": "jegem57974", "password": "Admin123!", "proxy": "http://nfrvpwlvajujbee96234-zone-resi-region-kz-st-abairegion-city-semey:hayfcmmpcg@resi-as.lightningproxies.net:9999"},
]

# Path to the folder containing videos
video_folder = "folder"
videos = sorted(os.listdir(video_folder))  # Ensure a consistent order of videos

# File to keep track of video history
history_file = "upload_history.json"

# Initialize history if it doesn't exist
if not os.path.exists(history_file):
    print("History file not found. Initializing a new one...")
    upload_history = {account["username"]: [] for account in accounts}
    with open(history_file, "w") as file:
        json.dump(upload_history, file)
else:
    try:
        with open(history_file, "r") as file:
            upload_history = json.load(file)
    except json.JSONDecodeError:
        print("History file is corrupted. Reinitializing...")
        upload_history = {account["username"]: [] for account in accounts}
        with open(history_file, "w") as file:
            json.dump(upload_history, file)

# Function to find the next video for an account
def get_next_video(account_username):
    history = upload_history[account_username]
    for video in videos:
        if video not in history:
            return video
    return None  # If all videos have been uploaded, return None

# Upload videos to accounts
for i, account in enumerate(accounts):
    cl = Client()
    cl.set_proxy(account["proxy"])
    cl.login(account["username"], account["password"])

    # Determine the next video to upload
    next_video = get_next_video(account["username"])
    if next_video:
        video_path = os.path.join(video_folder, next_video)
        cl.video_upload(video_path, caption=f"Video uploaded by {account['username']}")

        # Update history
        upload_history[account["username"]].append(next_video)
        with open(history_file, "w") as file:
            json.dump(upload_history, file)
        
        print(f"Uploaded {next_video} to {account['username']}")
    else:
        print(f"All videos have already been uploaded to {account['username']}. Skipping.")

    cl.logout()

print("Upload process completed.")
