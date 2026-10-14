import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DATABASE_FILE = 'bot_database.db'

    async def get_leaderboard_data(self, guild_id, event_type):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()

        query = '''
        SELECT u.user_id, u.wins, u.losses, MAX(e.timestamp_utc) as last_event
        FROM statistics u
        JOIN events e ON u.guild_id = e.guild_id AND u.user_id = e.user_id
        WHERE u.guild_id = ? AND e.event_type = ?
        GROUP BY u.user_id
        ORDER BY {} DESC, last_event DESC, u.user_id
        LIMIT 10'''.format('wins' if event_type == 'win' else 'losses')

        cursor.execute(query, (guild_id, event_type))
        results = cursor.fetchall()
        conn.close()
        return results

    async def create_leaderboard_embed(self, guild_id, event_type):
        guild = self.bot.get_guild(guild_id)
        data = await self.get_leaderboard_data(guild_id, event_type)

        embed = discord.Embed(
            title=f"{'WINS' if event_type == 'win' else 'LOSES'} LEADERBOARD",
            color=discord.Color.from_rgb(0, 0, 0)
        )

        if not data:
            embed.description = f"No {'wins' if event_type == 'win' else 'losses'} have been recorded."
        else:
            for i, (user_id, wins, losses, last_event) in enumerate(data, start=1):
                user = guild.get_member(user_id)
                if user:
                    value = f"Username: {user.display_name}\n"
                    value += f"{'Wins' if event_type == 'win' else 'Losses'}: {wins if event_type == 'win' else losses}\n"
                    value += f"Last {'win' if event_type == 'win' else 'loss'}: {datetime.strptime(last_event, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M') if last_event else 'No timestamp recorded'}"
                    embed.add_field(name=f"Rank {i}", value=value, inline=False)

        embed.set_footer(text="Made by Becali.18m")
        return embed

    async def update_leaderboard_message(self, guild_id, event_type):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT channel_id, wins_message_id, losses_message_id
        FROM leaderboard_messages
        WHERE guild_id = ?''', (guild_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            channel_id, wins_msg_id, losses_msg_id = result
            channel = self.bot.get_channel(channel_id)

            if channel:
                embed = await self.create_leaderboard_embed(guild_id, event_type)
                message_id = wins_msg_id if event_type == 'win' else losses_msg_id
                try:
                    message = await channel.fetch_message(message_id)
                    await message.edit(embed=embed)
                except discord.NotFound:
                    # Message was deleted, create a new one
                    message = await channel.send(embed=embed)
                    conn = sqlite3.connect(self.DATABASE_FILE)
                    cursor = conn.cursor()

                    if event_type == 'win':
                        cursor.execute('''
                        UPDATE leaderboard_messages
                        SET wins_message_id = ?
                        WHERE guild_id = ?''', (message.id, guild_id))
                    else:
                        cursor.execute('''
                        UPDATE leaderboard_messages
                        SET losses_message_id = ?
                        WHERE guild_id = ?''', (message.id, guild_id))

                    conn.commit()
                    conn.close()

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))