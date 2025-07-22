import requests  # search function & web
from dotenv import load_dotenv
import os


# load variables from .env file
load_dotenv("API_KEY.env")

# get my API key from my environment variable file
API_KEY = os.getenv("YOUTUBE_API_KEY")

print("Current working directory:", os.getcwd())
print("Environment variable YOUTUBE_API_KEY:", os.getenv("YOUTUBE_API_KEY"))

def search_youtube(query):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": API_KEY,
        "type": "video",  # search for videos only
        "maxResults": 5,
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        return results["items"]
    else: #to print error codes
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None


search_results = search_youtube("Your Search Query")

if search_results:
    for item in search_results:
        
        video_id = item["id"].get("videoId", None)
        if video_id:
            print(f"Title: {item['snippet']['title']}, URL: https://www.youtube.com/watch?v={video_id}")
        else:
            print(f"Video ID not found for item: {item['snippet']['title']}")
else:
    print("No results found")



