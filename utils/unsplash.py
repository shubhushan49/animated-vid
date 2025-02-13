import requests
from dotenv import load_dotenv
import os
from pathlib import Path

parent_path = Path(__file__).parent.parent
load_dotenv(dotenv_path=parent_path / ".env")

pics_path = parent_path / "pics"
if not pics_path.exists():
    os.makedirs(pics_path, exist_ok=True)

BASE_URL = "https://api.unsplash.com"
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
SECRET_KEY = os.getenv("UNSPLASH_SECRET_KEY")

def download_images(tag):
    tag_path = pics_path / tag
    if not (tag_path).exists():
        os.makedirs(tag_path, exist_ok=True)
    r = requests.get(f"{BASE_URL}/photos/random?client_id={ACCESS_KEY}&count=30&query=love")
    metadata = r.json()

    for i, photo_metadata in enumerate(metadata):
        img_url = photo_metadata["urls"]["full"]

        with open(tag_path / f"{i}.jpg", "wb") as f:
            img = requests.get(img_url)
            f.write(img.content)
            print(f"Image {i} downloaded")
