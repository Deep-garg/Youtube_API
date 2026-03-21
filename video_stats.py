import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path = './.env')

API_KEY = os.getenv("API_KEY")
print(API_KEY)

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

if __name__ == "__main__":
    get_playlist_id()


