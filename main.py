import discord
from discord.ext import commands
import os
import logging
from threading import Thread
from flask import Flask

# Set up logging
logging.basicConfig(level=logging.INFO)

# Flask app to keep the bot alive on Render
app = Flask('')

@app.route('/')
def home():
    return "Discord Bot OK"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Bot setup
TOKEN = os.environ['DISCORDKEY']
intents = discord.Intents.default()
intents.members = True  # For role management
intents.message_content = True  # Needed for command processing
bot = commands.Bot(command_prefix='!', intents=intents)

# Event when bot is ready
@bot.event
async def on_ready():
    logging.info("Bot is live")  # Prints to Render logs
    # Send "Bot is live" to a specific channel
    channel = bot.get_channel(YOUR_CHANNEL_ID_HERE)  # Replace with your channel ID
    if channel:
        try:
            await channel.send("Bot is live")
            logging.info(f"Sent 'Bot is live' to channel {channel.name}")
        except Exception as e:
            logging.error(f"Failed to send message to channel: {str(e)}")
    else:
        logging.warning("Channel not found or bot lacks access")
    print(f'{bot.user} has connected to Discord!')

# Simple ping command (no owner restriction)
@bot.command(name="ping")
async def ping(ctx):
    """Responds with Pong! to test if bot is working"""
    await ctx.send("Pong!")
    logging.info("Ping command executed")

# Owner-only command example
def is_owner():
    def predicate(ctx):
        return ctx.author.id == 274753853516283905  # Replace with your ID if needed
    return commands.check(predicate)

@bot.command(name="testowner")
@is_owner()
async def test_owner(ctx):
    await ctx.send("✅ You have permission to use owner-only commands!")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Command error: {str(error)}")
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ You don’t have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please provide all required arguments!")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")

# Start the web server and bot
keep_alive()
bot.run(TOKEN)