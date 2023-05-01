import os

import discord
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
from dotenv import load_dotenv
from discord.ext import commands
import random
import requests
import imageio
import json
import textwrap
import nltk.corpus

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tspeak(self, ctx):
        message = ctx.message
        # Get the message that the user replied to
        replied_message = message.reference.resolved if message.reference else None
        if replied_message:
            # Check if the user replied to a message
            try:
                folder = 'talking'
                images = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]
                if images:
                    await replied_message.reply(file=discord.File(random.choice(images)))
                else:
                    await message.reply("No images found.")
            except FileNotFoundError:
                await ("File not found")
        else:
            await message.reply("Please reply to a message with !t")

