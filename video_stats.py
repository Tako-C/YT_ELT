import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
API_KEY = os.getenv("API_KEY")

max_results = 50


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
    

playlisId = get_playlist_id()

def get_videos_in_playlist(playlist_id):
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            
            pageToken = data.get("nextPageToken")

            if not pageToken:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    get_playlist_id() ## prints the playlist ID
    print(get_videos_in_playlist(playlisId)) ## List of video IDs in the playlist