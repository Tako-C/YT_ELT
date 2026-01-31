from datetime import date
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

def get_video_ids(playlist_id):
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
    
def batch_list(video_id_list, batch_size):
    for video_id in range(0,len(video_id_list), batch_size):
        yield video_id_list[video_id:video_id + batch_size]


def extract_video_data(video_id_list):
    extracted_data = []
    try:
        for batch in batch_list(video_id_list,max_results):
            video_id_list_str = ",".join(batch)
            print(f"Processing batch: {video_id_list_str}")
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id_list_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()

            for item in data.get("items", []):
                video_data = {
                    "video_id": item["id"],
                    "title": item["snippet"].get("title"),
                    "publishedAt": item["snippet"].get("publishedAt"),
                    "duration": item["contentDetails"].get("duration"),
                    "viewCount": item["statistics"].get("viewCount"),
                    "likeCount": item["statistics"].get("likeCount"),
                    "commentCount": item["statistics"].get("commentCount"),
                }

            extracted_data.append(video_data)
        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"
    with open(file_path, "w" , encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4 ,ensure_ascii=False)

if __name__ == "__main__":
    playlisId = get_playlist_id()
    video_ids = get_video_ids(playlisId)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)


