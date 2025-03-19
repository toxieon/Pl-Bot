import discord
from discord.ext import commands
import os
import webserver

# Load environment variables
TOKEN = os.environ['DISCORDKEY']

# Set up bot with command prefix and intents
intents = discord.Intents.default()
intents.members = True  # Needed for role management
bot = commands.Bot(command_prefix='-', intents=intents)

# Event to show when bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Check for admin role
def is_admin():
    def predicate(ctx):
        # Check if user has a role named "Admin"
        return any(role.name.lower() == "admin" for role in ctx.author.roles)
    return commands.check(predicate)

# Role creation command
@bot.command(name='createrole')
@is_admin()
async def create_role(ctx, role_name: str):
    """Creates a new role with the specified name"""
    try:
        await ctx.guild.create_role(name=role_name)
        await ctx.send(f'✅ Role "{role_name}" created successfully!')
    except Exception as e:
        await ctx.send(f'❌ Error creating role: {str(e)}')

# Role deletion command
@bot.command(name='delrole')
@is_admin()
async def delete_role(ctx, role: discord.Role):
    """Deletes the specified role"""
    try:
        await role.delete()
        await ctx.send(f'✅ Role "{role.name}" deleted successfully!')
    except Exception as e:
        await ctx.send(f'❌ Error deleting role: {str(e)}')

# Role color change command
@bot.command(name='rolecolor')
@is_admin()
async def change_role_color(ctx, role: discord.Role, color_hex: str):
    """Changes the color of a specified role (use hex code like #FF0000)"""
    try:
        # Remove # if present and convert hex to integer
        color_hex = color_hex.replace('#', '')
        color = discord.Color(int(color_hex, 16))
        await role.edit(color=color)
        await ctx.send(f'✅ Color updated for role "{role.name}"!')
    except ValueError:
        await ctx.send('❌ Please use a valid hex color code (e.g., #FF0000 for red)')
    except Exception as e:
        await ctx.send(f'❌ Error changing color: {str(e)}')

# Text channel creation command
@bot.command(name='createtext')
@is_admin()
async def create_text_channel(ctx, channel_name: str):
    """Creates a new text channel with the specified name"""
    try:
        await ctx.guild.create_text_channel(channel_name)
        await ctx.send(f'✅ Text channel "{channel_name}" created successfully!')
    except Exception as e:
        await ctx.send(f'❌ Error creating text channel: {str(e)}')

# Text channel deletion command
@bot.command(name='deltext')
@is_admin()
async def delete_text_channel(ctx, channel: discord.TextChannel):
    """Deletes the specified text channel"""
    try:
        await channel.delete()
        await ctx.send(f'✅ Text channel "{channel.name}" deleted successfully!')
    except Exception as e:
        await ctx.send(f'❌ Error deleting text channel: {str(e)}')

# Voice channel creation command
@bot.command(name='createvoice')
@is_admin()
async def create_voice_channel(ctx, channel_name: str):
    """Creates a new voice channel with the specified name"""
    try:
        await ctx.guild.create_voice_channel(channel_name)
        await ctx.send(f'✅ Voice channel "{channel_name}" created successfully!')
    except Exception as e:
        await ctx.send(f'❌ Error creating voice channel: {str(e)}')

# Voice channel deletion command
@bot.command(name='delvoice')
@is_admin()
async def delete_voice_channel(ctx, channel: discord.VoiceChannel):
    """Deletes the specified voice channel"""
    try:
        await channel.delete()
        await ctx.send(f'✅ Voice channel "{channel.name}" deleted successfully!')
    except Exception as e:
        await ctx.send(f'❌ Error deleting voice channel: {str(e)}')

# Error handling for missing permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('❌ You need the Admin role to use this command!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Please provide all required arguments!')
    else:
        await ctx.send(f'❌ An error occurred: {str(error)}')


# webserver
webserver.keep_alive()
# Run the bot
bot.run(TOKEN)