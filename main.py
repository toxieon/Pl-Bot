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

# Discord channel to announce bot startup (REPLACE WITH ACTUAL CHANNEL ID)
CHANNEL_ID = 123456789012345678  # Replace with your real channel ID


# Event when bot is ready
@bot.event
async def on_ready():
    logging.info(f"Bot {bot.user} is live!")

    # Send "Bot is live" to a specific channel
    channel = bot.get_channel(CHANNEL_ID)  # Correctly gets channel
    if channel:
        try:
            await channel.send("✅ Bot is live and ready!")
            logging.info(f"Sent 'Bot is live' to channel {channel.name}")
        except Exception as e:
            logging.error(f"Failed to send message to channel: {str(e)}")
    else:
        logging.warning("❌ Channel not found or bot lacks access")

        @bot.command(name="createtext")
        async def create_text_channel(ctx, channel_name: str):
            """Creates a new text channel with the specified name"""
            try:
                guild = ctx.guild  # Get the server (guild)
                existing_channel = discord.utils.get(guild.channels, name=channel_name)

                if existing_channel:
                    await ctx.send(f"❌ A channel named #{channel_name} already exists!")
                else:
                    new_channel = await guild.create_text_channel(channel_name)
                    await ctx.send(f"✅ Text channel **#{new_channel.name}** created successfully!")
                    logging.info(f"Created text channel: #{new_channel.name}")

            except discord.Forbidden:
                await ctx.send("❌ I don't have permission to create channels!")
                logging.error("Bot lacks permission to create channels.")

            except Exception as e:
                await ctx.send(f"❌ Error creating channel: {str(e)}")
                logging.error(f"Error creating text channel: {str(e)}")


# Simple ping command (no owner restriction)
@bot.command(name="ping")
async def ping(ctx):
    """Responds with Pong! to test if bot is working"""
    await ctx.send("Pong!")
    logging.info("Ping command executed")


# Restrict commands to bot owner only
def is_owner():
    def predicate(ctx):
        return ctx.author.id == 274753853516283905  # Your ID restored

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
