import requests
import os
from dotenv import load_dotenv

load_dotenv("./.env")  # Load environment variables from .env file
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")


def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={CHANNEL_HANDLE}&key={API_KEY}"
        
        response = requests.get(url)

        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        channel_items = data["items"][0]

        channel_playlist_id = channel_items["id"]

        # print(f"Playlist ID for channel {CHANNEL_HANDLE}: {channel_playlist_id}")

        return channel_playlist_id
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching playlist ID: {e}")
        return None

if __name__ == "__main__":
    get_playlist_id()
    