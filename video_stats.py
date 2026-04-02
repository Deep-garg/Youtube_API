import requests
import json
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv(dotenv_path = './.env')

API_KEY = os.getenv("API_KEY")

maxResults = 50

CHANNEL_HANDLE = 'SoniaGarg'

def get_playlist_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()
        playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        print(playlist_id)
        return playlist_id

    except requests.exceptions.RequestException as e:
        raise e

def get_video_Id(channel_playlist_id):
    video_ids = []
    pageToken = None

    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={channel_playlist_id}&key={API_KEY}'
    
    try:
        while True:
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            pageToken = data.get('nextPageToken')

            if not pageToken:
                break  

        print(len(video_ids))
        return video_ids         

    except requests.exceptions.RequestException as e:
        raise e



def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id : video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_id_str = ','.join(batch)
        url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id_str}&key={API_KEY}'
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('items', []):
            video_id = item['id']
            snippet = item['snippet']
            contentDetails = item['contentDetails']
            statistics = item['statistics']

            video_data = {
                'video_id' : video_id,
                'title' : snippet['title'],
                'publishedAt' : snippet['publishedAt'],
                'duration' : contentDetails['duration'],
                'viewCount' : statistics.get('viewCount', None),
                'likeCount' : statistics.get('likeCount', None),
                'commentCount' : statistics.get('commentCount', None)
            }

            extracted_data.append(video_data)
        
        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e
    
def save_to_json(extracted_data):
    file_path = f'./data/youtube_api{date.today()}.json'

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii= False)


if __name__ == "__main__":
    channel_playlist_id = get_playlist_id()
    videos_id = get_video_Id(channel_playlist_id)
    final_video_data = extract_video_data(videos_id)
    save_to_json(final_video_data)


