# Ryle
Music Bot for Discord

This is a Discord bot built with 
Nextcord (https://nextcord.readthedocs.io/en/stable/) and 
yt-dlp (https://github.com/yt-dlp/yt-dlp) 
that allows users to play music from YouTube in a Discord voice channel.

Features

- Join and leave voice channels
- Play, pause, resume, and stop music
- Adjust the volume of the bot
- Support for streaming from YouTube links

Requirements

- Python 3.8 or higher
- Nextcord (https://nextcord.readthedocs.io/en/stable/)
- yt-dlp (https://github.com/yt-dlp/yt-dlp)
- FFmpeg(https://ffmpeg.org/) (required for audio playback)

Installation

1. Clone the repository:
    
    git clone https://github.com/yourusername/music-bot.git
    cd music-bot
   

2. Create a virtual environment and activate it:
    - On Windows:
      
      - python -m venv venv
      - .\venv\Scripts\activate
      
    - On macOS/Linux:
      
      - python3 -m venv venv
      - source venv/bin/activate
      

3. Install the required dependencies:
    
    pip install -r requirements.txt
    

4. Ensure FFmpeg is installed and accessible in your system's PATH. 
Install FFmpeg from https://ffmpeg.org/download.html if you haven't already.

5. Add your bot token to the script:
    - Replace `YOUR APP TOKEN` in the `bot.run("YOUR APP TOKEN")` line with your actual bot token.

6. Run the bot:
    
    python musicbot.py
    

Commands

- /play (name_of_the_song) : Plays the music you provided the name of
- /join: Makes the bot join the voice channel.
- /leave: Makes the bot leave the voice channel.
- /play (url): Plays the music from the provided YouTube URL.
- /pause: Pauses the music.
- /resume: Resumes the music.
- /stop: Stops the music.
- /volume <volume>: Adjusts the bot's volume (0 to 100).

License

This project is licensed under the MIT License - see the LICENSE file for details.


