import nextcord
from nextcord.ext import commands
import yt_dlp as youtube_dl
import asyncio

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -ar 48000 -b:a 512k',
    'executable': r'G:\ffmpeg\bin\ffmpeg.exe'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

intents = nextcord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Required for voice state updates

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.sync_all_application_commands()  # Sync slash commands globally

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel and not after.channel:
        if not any(vc.is_playing() for vc in bot.voice_clients):
            await bot.close()

# Slash Commands Below ⚡
@bot.slash_command(description="Join your voice channel")
async def join(interaction: nextcord.Interaction):
    """Join the user's voice channel"""
    if not interaction.user.voice:
        return await interaction.response.send_message("⚠️ You're not in a voice channel!", ephemeral=True)
    
    channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.response.send_message(f"✅ Joined {channel.mention}")

@bot.slash_command(description="Leave the voice channel")
async def leave(interaction: nextcord.Interaction):
    """Leave the current voice channel"""
    voice_client = interaction.guild.voice_client
    if not voice_client:
        return await interaction.response.send_message("⚠️ I'm not in a voice channel!", ephemeral=True)
    
    await voice_client.disconnect()
    await interaction.response.send_message("✅ Left the voice channel")

@bot.slash_command(description="Play a song from YouTube")
async def play(interaction: nextcord.Interaction, query: str):
    """Play audio from a YouTube URL"""
    await interaction.response.defer()  # Acknowledge the interaction first
    
    # Ensure the bot is in a voice channel
    if not interaction.guild.voice_client:
        if interaction.user.voice:
            await interaction.user.voice.channel.connect()
        else:
            return await interaction.followup.send("⚠️ You must be in a voice channel!", ephemeral=True)
    
    # Stop current track if playing
    voice_client = interaction.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    
    # Play new track
    player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
    voice_client.play(player, after=lambda e: print(f'Error: {e}') if e else None)
    await interaction.followup.send(f"🎶 Now playing: **{player.title}**")

@bot.slash_command(description="Pause the current song")
async def pause(interaction: nextcord.Interaction):
    """Pause playback"""
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        return await interaction.response.send_message("⚠️ Nothing is playing!", ephemeral=True)
    
    voice_client.pause()
    await interaction.response.send_message("⏸️ Playback paused")

@bot.slash_command(description="Resume playback")
async def resume(interaction: nextcord.Interaction):
    """Resume paused playback"""
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_paused():
        return await interaction.response.send_message("⚠️ Playback isn't paused!", ephemeral=True)
    
    voice_client.resume()
    await interaction.response.send_message("▶️ Playback resumed")

@bot.slash_command(description="Stop playback and clear queue")
async def stop(interaction: nextcord.Interaction):
    """Stop the music"""
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        return await interaction.response.send_message("⚠️ Nothing is playing!", ephemeral=True)
    
    voice_client.stop()
    await interaction.response.send_message("⏹️ Playback stopped")

@bot.slash_command(description="Adjust volume (0-200%)")
async def volume(interaction: nextcord.Interaction, level: int = nextcord.SlashOption(description="Volume percentage", min_value=0, max_value=200)):
    """Change playback volume"""
    voice_client = interaction.guild.voice_client
    if not voice_client:
        return await interaction.response.send_message("⚠️ Not in a voice channel!", ephemeral=True)
    
    voice_client.source.volume = level / 100
    await interaction.response.send_message(f"🔊 Volume set to **{level}%**")

bot.run("YOUR_BOT_TOKEN")
