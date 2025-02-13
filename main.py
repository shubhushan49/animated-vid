from TTS.api import TTS
from utils.db_models import Quotes, ENGINE, GoodQuotes
from utils.scraper import GoodReads
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import json
from pathlib import Path
import os
import numpy as np
import ffmpeg
import random
import shutil

# Get device
# device = "mps" if torch.mps.is_available() else "cpu"
device = "cpu"

working_models = ["tts_models/en/jenny/jenny"]

Session = sessionmaker(bind=ENGINE)
session = Session()

def models_to_json():
    models = TTS().list_models().list_tts_models()
    with open("model_names.json", "w") as f:
        f.write(json.dumps(models, indent=4))

def create_video_with_audio(video_path, audio_path, output_video_path, fps=30):
    # Probe audio to get its duration
    audio_info = ffmpeg.probe(audio_path)
    audio_duration = float(next(s for s in audio_info['streams'] if s['codec_type'] == 'audio')['duration'])

    # Crop the video to match the audio duration
    video_stream = ffmpeg.input(video_path)
    video_stream = ffmpeg.trim(video_stream, duration=audio_duration).setpts('PTS-STARTPTS')
    
    # Load the audio stream
    audio_stream = ffmpeg.input(audio_path)
    
    # Combine video and audio, ensuring synchronization
    output = ffmpeg.output(
        video_stream, audio_stream, output_video_path, 
        vcodec='libx264', acodec='aac', strict='experimental'
    )
    
    # Execute ffmpeg command
    output.run()

    # Move the final output video to the "video" folder
    shutil.move(
        Path(output_video_path),
        Path(__file__).parent / "video" / output_video_path
    )


def create_video(tag, audio_path, vid_id):
    # video path
    video_path = Path(__file__).parent / "video"
    if not video_path.exists():
        os.makedirs(video_path, exist_ok=True)
    vid_tags = Path(__file__).parent / "pexels_vids" / tag
    vids = os.listdir(vid_tags)
    vid = random.choice(vids)
    vid_path = vid_tags / vid
    create_video_with_audio(vid_path, audio_path, f"{vid_id}.mp4")

def quote_to_video():
    output_folder = Path(__file__).parent / "audio"
    if not output_folder.exists():
        os.makedirs(output_folder, exist_ok=True)
    files_lst = [int(file.split(".")[0]) for file in os.listdir(output_folder)]
    quotes_db = session.query(GoodQuotes).filter(
        and_(
            GoodQuotes.vid_shown == False,
            ~GoodQuotes.id.in_(files_lst)
            )
        )
    for quote in quotes_db:
        tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(device)
        tts.tts_to_file(quote.quote, file_path= output_folder / f"{quote.id}.wav")
        print(f"{quote.id} converted to audio")
        create_video(quote.tag, output_folder / f"{quote.id}.wav", quote.id)
        print(f"{quote.id} converted to video")

def main():
    good = GoodReads()
    good.get_quote_from_tags()
    quote_to_video()


if __name__ == "__main__":
    main()