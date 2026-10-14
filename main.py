import discord
from discord.ext import commands
import os
import asyncio
import sqlite3
from datetime import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

DATABASE_FILE = 'bot_database.db'

# Database setup
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS statistics (
        guild_id INTEGER,
        user_id INTEGER,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        PRIMARY KEY (guild_id, user_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        user_id INTEGER,
        event_type TEXT,
        timestamp_utc TEXT,
        moderator_id INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard_messages (
        guild_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        wins_message_id INTEGER,
        losses_message_id INTEGER
    )''')

    conn.commit()
    conn.close()

# Leaderboard refresh
async def refresh_leaderboards():
    while True:
        await asyncio.sleep(60)
        # Implement leaderboard refresh logic

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    init_db()
    bot.loop.create_task(refresh_leaderboards())

async def setup_hook(self):
    await self.load_extension('cogs.commands')
    await self.load_extension('cogs.leaderboard')

    # Sync slash commands
    await self.tree.sync()

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))