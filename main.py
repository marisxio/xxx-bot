import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True  # Needed for commands
intents.members = True  # Needed to detect member joins

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_member_join(member):
    # Change this to your welcome channel name
    channel = discord.utils.get(member.guild.text_channels, name="🛍️")
    if channel:
        await channel.send(f"🎉 Welcome to the server, {member.mention}! We're so happy you're here! 💖")

@bot.command()
async def testgreet(ctx):
    """Sends a test welcome message to the welcome channel."""
    channel = discord.utils.get(ctx.guild.text_channels, name="🛍️")
    if channel:
        await ctx.send(f"🎉 Welcome to the server, {ctx.author.mention}! We're so happy you're here! 💖")
        await ctx.send("Test welcome message sent!")
    else:
        await ctx.send("❌ Welcome channel not found.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Deletes a specified number of messages."""
    if amount < 1:
        await ctx.send("Please specify a positive number of messages to delete.")
        return
    deleted = await ctx.channel.purge(limit=amount)
    confirmation = await ctx.send(f"🧹 Deleted {len(deleted)} messages!")
    await confirmation.delete(delay=5)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to manage messages.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Please provide a valid number of messages to delete.")
    else:
        await ctx.send("❌ An error occurred.")

# === Flask keep_alive web server ===
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
# === End keep_alive setup ===

bot.run(os.getenv("MTM5NDkyMzIyNzU0MDc1MDQyNw.GxbTR6.7_PIKOpy7475nfSeYtY3efFxgMXKsB8ZEvNC9w"))
