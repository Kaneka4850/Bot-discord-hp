import discord

async def send_dm(user: discord.User, message: str):
    try:
        await user.send(message)
        return True
    except discord.Forbidden:
        return False