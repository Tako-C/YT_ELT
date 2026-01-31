import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
API_KEY = os.getenv("API_KEY")


CHANAL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANAL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        # print(f"response: {response}")

        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        # print(json.dumps(data, indent=4))

        # data.items[0].contentDetails.relatedPlaylists.uploads
        channal_item = data["items"][0]
        chanal_playlisId = channal_item["contentDetails"]["relatedPlaylists"]["uploads"]

        print(f"chanal_playlisId: {chanal_playlisId}")
        return chanal_playlisId

    except requests.exceptions.RequestException as e:
        raise e
if __name__ == "__main__":
    get_playlist_id()