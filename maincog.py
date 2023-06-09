import os

import discord
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from dotenv import load_dotenv
from discord.ext import commands
import random

class MainCog(commands.Cog):
    def __init__(self, bot):
        """
        Standard init method

        Args:
            self: the cog itself
            bot: the bot
        """
        self.bot = bot

    @commands.command()
    async def tspeak(self, ctx):
        """
        Triggers upon !t command, which, on user reply to a message, the bot
        replies to that message with a Revue Starlight frame with a speech bubble

        Args:
            ctx (context): "context" containing info about command message
        """
        message = ctx.message
        replied_message = message.reference.resolved if message.reference else None
        if replied_message:
            try:
                folder = 'talking'
                images = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]
                if images:
                    await message.delete() 
                    await replied_message.reply(file=discord.File(random.choice(images)))
                    await replied_message.channel.send(f"(!t used by {message.author.name})")
                else:
                    await message.reply("No images found.")
            except FileNotFoundError:
                await ("File not found")
        else:
            await message.reply("Please reply to a message with !t")

