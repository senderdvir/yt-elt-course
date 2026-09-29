import requests
import os
from dotenv import load_dotenv

load_dotenv("./.env")  # Load environment variables from .env file
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
MAX_RESULTS = 50  # Maximum number of results to fetch
PLAYLIST_ID = os.getenv("PLAYLIST_ID")


def get_playlist_id():
    """
    Fetches the playlist ID for a given YouTube channel using the YouTube Data API.
    Returns:
        str: The playlist ID for the specified channel."""
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
    
def get_videos_id() -> list[str]:
    """Fetches video IDs from a YouTube playlist using the YouTube Data API.
    Returns:
        list[str]: A list of video IDs from the specified playlist.
    """

    next_page_token = None
    video_items: list[str] = []
    while True:

        base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={PLAYLIST_ID}&maxResults={MAX_RESULTS}&key={API_KEY}"
        
        if next_page_token:

            base_url += f"&pageToken={next_page_token}"

        try:
            response = requests.get(base_url)
                
            response.raise_for_status()  # Raise an exception for HTTP errors
                
            data = response.json()
                
            for item in data.get("items", []):

                video_id = item["contentDetails"]["videoId"]

                video_items.append(video_id)
                
            next_page_token = data.get("nextPageToken")
                
            if not next_page_token:

                break

        except requests.exceptions.RequestException as e:

            print(f"Error occurred while fetching video IDs: {e}")

            return video_items
        
    return video_items


if __name__ == "__main__":
    print(get_videos_id())
    