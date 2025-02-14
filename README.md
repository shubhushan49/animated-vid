# What's the project about?
If I have to be honest, it is not something extraordinary nor is it very difficult.

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