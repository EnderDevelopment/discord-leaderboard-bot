# Discord Leaderboard Bot

Track wins and losses with automatic leaderboards in Discord

## Features

- Track wins and losses for users
- Automatically update leaderboards
- Display top 10 users by wins and losses

## Requirements

- Python 3.8 or higher
- discord.py
- python-dotenv
- aiosqlite

## Installation

1. Clone the repository
2. Install the required packages: `pip install -r requirements.txt`
3. Create a `.env` file based on `.env.example` and fill in your Discord bot token and channel ID
4. Run the bot: `python main.py`

## Usage

### Commands

| Command | Description | Permissions |
|---------|-------------|-------------|
| !addwin @user | Add a win to a user | Administrator |
| !addlose @user | Add a loss to a user | Administrator |
| !leaderboardwins | Display the wins leaderboard | Everyone |
| !leaderboardloses | Display the losses leaderboard | Everyone |

### Configuration

Create a `.env` file with the following variables:

```env
DISCORD_TOKEN=your_discord_bot_token_here
LEADERBOARD_CHANNEL_ID=your_channel_id_here
```

---

## Generated with EnderDevelopment

This plugin was generated in minutes with [EnderDevelopment](https://enderdevelopment.com) — the AI platform that turns your ideas into working Minecraft plugins, Discord bots and FiveM scripts.

**Want your own?** [Generate this project on EnderDevelopment](https://dash.enderdevelopment.com?utm_source=github&utm_medium=readme&utm_campaign=discord-leaderboard-bot&utm_content=bottom) — describe it in one sentence and get the full source code.