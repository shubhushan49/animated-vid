import requests
from dotenv import load_dotenv
import os
from pathlib import Path
import json

parent_path = Path(__file__).parent.parent
load_dotenv(dotenv_path=parent_path / ".env")

pexel_vids_path = parent_path / "pexels_vids"
if not pexel_vids_path.exists():
    os.makedirs(pexel_vids_path, exist_ok=True)

BASE_URL = "https://api.pexels.com/videos/search"
API_KEY = os.getenv("PEXELS_API_KEY")
HEADERS = {"Authorization": API_KEY}
def download_videos(tag):
    tag_path = pexel_vids_path / tag
    if not tag_path.exists():
        os.makedirs(tag_path, exist_ok=True)
    r = requests.get(f"{BASE_URL}?query={tag}&per_page=20&orientation=potrait", headers=HEADERS)

    result = r.json()

    vids_metadata = [x.get("video_files") for x in result["videos"]]
    for i, vid_files in enumerate(vids_metadata):
        for vid_quality in vid_files:
            if vid_quality.get("quality") == "hd":
                vid_url = vid_quality.get("link")
                with open(tag_path / f"{i}.mp4", "wb") as f:
                    vid = requests.get(vid_url)
                    f.write(vid.content)
                    print(f"Video downloaded {i}.mp4")
                break
    

def test():
    tag_path = pexel_vids_path / "love"
    if not tag_path.exists():
        os.makedirs(tag_path, exist_ok=True)
    with open("pexels.json", "r") as f:
        data = json.load(f)
        vids_metadata = [x.get("video_files") for x in data["videos"]]
        for i, vid_files in enumerate(vids_metadata):
            for vid_quality in vid_files:
                if vid_quality.get("quality") == "hd":
                    vid_url = vid_quality.get("link")
                    with open(tag_path / f"{i}.mp4", "wb") as f:
                        vid = requests.get(vid_url)
                        f.write(vid.content)
                        print(f"Video downloaded")
                    break

if __name__ == "__main__":
    # download_videos("love")
    test()