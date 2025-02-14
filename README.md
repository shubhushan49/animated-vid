# What's the project about?
The project is about automating the creation of Potrait videos from Quotes scraped from the internet. I got this idea while watching reels on instagram. Some of the accounts posted interesting stories from reddit, the background was a random clip from minecraft and the audio was created with an AI. I got a similar idea, and created this project.

## Todo
- The TTS is not performant, it requires a lot of resources, and the output is not that great either. However, I have seen some reels in instagram that have a lower quality speech.
- For elaborate videos, one can use solutions like the models from elevenlabs.
- Optimize the scraping process:
    - Current approach
        - For every run the scraper scrapes the data
    - Better approach
        - Check the database, if there are quotes that don't have vid_shown=True, then just use them until they are exhausted before scraping

## [Scraper](utils/scraper.py)
### Zenquotes
Get a random quote from [zenquotes](https://zenquotes.io/api/quotes/) api
### GoodReads
- Select a random quote tag
- Navigate to a random page, in the range 1-100
- Get all the quotes in the page
- Download the videos that closely relate to the quote tag from pexels

## [DB Models](utils/db_models.py)
### Quotes
    Cols: id, quote, widget_shown, vid_shown
## Good Quotes
    Cols: id, tag, quote, widget_shown, vid_shown, page

## [Workflow](main.py)
- Scrape quotes from Good Reads
- Download related videos from pexels
- Use TTS to convert quote text to speech
- Use ffmpeg to combine a random video from pexels to the audio created with TTS

## Try it out
```bash
    git clone git@github.com:shubhushan49/animated-vid.git
    cd animated-vid/
    virtualenv venv && source venv/bin/activate
    pip3 install -r requirements.txt
    python3 main.py
```