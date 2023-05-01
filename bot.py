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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot = commands.Bot(intents=intents,command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='commands')
async def helpcommands(ctx):
    with open('commands.txt') as f:
        textcommands = f.read()
    await ctx.send(textcommands)

@bot.command(name='quote')
async def quote(ctx):
    with open('qotd.txt', encoding='utf-8') as f:
        quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

    # Get a random quote
    await ctx.send(random.choice(quotes))
    

@bot.command(name='revuegif')
async def revuegif(ctx):
    print('successful call')

    apikey = "AIzaSyA7f0xuVkCkyqdxKOPLUxsBh72xswUPjnU" 
    lmt = 1
    ckey = "mrwhitebot" 

    search_term = "revue starlight"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s&random=true" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_8gifs['results']]
        await ctx.send("\n".join(gif_urls))
    else:
        top_8gifs = None

@bot.command(name='gm')
async def good_morning(ctx):
    print('successful call')
    apikey = "AIzaSyA7f0xuVkCkyqdxKOPLUxsBh72xswUPjnU"
    lmt = 2
    ckey = "mrwhitebot"

    search_term = "revue starlight good morning"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_2gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_2gifs['results']]
        random_url = random.choice(gif_urls)
        await ctx.send(random_url)
    else:
        await ctx.send('there was an error but good morning anyway')

@bot.command(name='ga')
async def good_afternoon(ctx):
    print('successful call')
    apikey = "AIzaSyA7f0xuVkCkyqdxKOPLUxsBh72xswUPjnU"
    lmt = 2
    ckey = "mrwhitebot"

    search_term = "revue starlight good afternoon"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_2gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_2gifs['results']]
        random_url = random.choice(gif_urls)
        await ctx.send(random_url)
    else:
        await ctx.send('there was an error but good afternoon anyway')

@bot.command(name='gn')
async def good_night(ctx):
    print('successful call')
    apikey = "AIzaSyA7f0xuVkCkyqdxKOPLUxsBh72xswUPjnU"
    lmt = 2
    ckey = "mrwhitebot"

    search_term = "revue starlight good night"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_2gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_2gifs['results']]
        random_url = random.choice(gif_urls)
        await ctx.send(random_url)
    else:
        await ctx.send('there was an error but good afternoon anyway')

@bot.command(name='mrwhite')
async def mrwhite(ctx):
    print('test')
    if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                if attachment.content_type.startswith('image/'):
                    image_data = await attachment.read()
                    await ctx.send('loading mr white image')
                    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    face_cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml')
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=1, minSize=(10, 10))

                    if len(faces) > 0:
                        img = Image.open(io.BytesIO(image_data)).convert('RGBA')
                        mr_white = Image.open("mrwhiteface.png").convert('RGBA')
                        for (x, y, w, h) in faces:
                            mr_white_resized = mr_white.resize((w, int(w * mr_white.size[1] / mr_white.size[0])), resample=Image.LANCZOS)
                            img.paste(mr_white_resized, (x, y), mr_white_resized)
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        await ctx.send(file=discord.File(fp=img_bytes, filename='mrwhiteface.png'))
                    else:
                         await ctx.send("no faces found")
    else:
        await ctx.send('please include an image to mr whiteify')


@bot.command(name='revueshitpostchar')
async def revueshitpostchar(ctx):
    print('successful call')
    # set the apikey and limit
    apikey = "AIzaSyA7f0xuVkCkyqdxKOPLUxsBh72xswUPjnU"  # click to set to your apikey
    lmt = 1
    ckey = "mrwhitebot"  # set the client_key for the integration and use the same value for all API calls

    # Load the list of words from the NLTK corpus
    words = nltk.corpus.words.words()

    # Select a random word from the list
    random_word = random.choice(words)

    # Use the random word as the search term
    search_term = random_word

    # get a random gif using the search term
    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s&random=true" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
        with open('quotes.txt') as f:
            quotes = f.read().splitlines()

        # Get a random quote
        random_quote = random.choice(quotes)

        loadingmessage = await ctx.send("loading randomly generated revue starlight shitpost")

        # Read the image/gif file
        all_formats= [gif['media_formats'] for gif in top_8gifs['results']]
        gif_url = all_formats[0]['mediumgif']['url']
        response = requests.get(gif_url)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))

        # Create the captioned image/gif
        caption = f'{random_quote.strip()}'
        image_with_caption = await create_image_with_caption(image, caption)

        # Send the captioned image/gif
        await ctx.send(file=image_with_caption)
        await loadingmessage.delete()
        return
    else:
        top_8gifs = None

@bot.command(name='revueshitpostquote')
async def revueshitpostquote(ctx):
    print('successful call')
    # set the apikey and limit
    apikey = "AIzaSyA7f0xuVkCkyqdxKOPLUxsBh72xswUPjnU"  # click to set to your apikey
    lmt = 1
    ckey = "mrwhitebot"  # set the client_key for the integration and use the same value for all API calls

    # Load the list of words from the NLTK corpus
    words = nltk.corpus.words.words()

    # Select a random word from the list
    random_word = random.choice(words)

    # Use the random word as the search term
    search_term = random_word

    # get a random gif using the search term
    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s&random=true" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_8gifs = json.loads(r.content)

        with open('qotd.txt', encoding='utf-8') as f:
            quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

        # Get a random quote
        random_quote = random.choice(quotes)

        loadingmessage = await ctx.send("loading randomly generated revue starlight shitpost")

        # Read the image/gif file
        all_formats= [gif['media_formats'] for gif in top_8gifs['results']]
        gif_url = all_formats[0]['mediumgif']['url']
        response = requests.get(gif_url)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))

        # Create the captioned image/gif
        caption = f'{random_quote.strip()}'
        image_with_caption = await create_image_with_caption(image, caption)

        # Send the captioned image/gif
        try:
            await ctx.send(file=image_with_caption)
        except discord.errors.HTTPException as error:
            await ctx.send("File was too large, try again")

        await loadingmessage.delete()
        return
    else:
        top_8gifs = None

@bot.command(name='revuecaption')
async def caption_image(ctx):
    # Get the most recent message sent by the user
    if len(ctx.message.attachments) == 0:
        async for message in ctx.channel.history(limit=2, before=ctx.message):
            # Check if the message contains any attachments
            if len(message.attachments) > 0:
                attachment = message.attachments[0]
                if attachment.content_type.startswith('image/') or attachment.content_type.startswith('video/'):
                    await ctx.send('loading revue starlight shitpost')
                    # Read quotes from file
                    with open('quotes.txt') as f:
                        quotes = f.read().splitlines()

                    # Get a random quote
                    random_quote = random.choice(quotes)

                    # Read the image/gif file
                    image_data = await attachment.read()
                    image = Image.open(io.BytesIO(image_data))
                    if image.format == 'GIF':
                        await ctx.send('the given image is a gif, may take a while')

                    # Create the captioned image/gif
                    caption = f'{random_quote.strip()}'
                    image_with_caption = await create_image_with_caption(image, caption)

                    # Send the captioned image/gif
                    await ctx.send(file=image_with_caption)
                    return
            elif len(message.content) > 0:
                print('message found')
                link = message.content.strip()
                print('link: ' + link)
                if link.endswith('.jpg') or link.endswith('.jpeg') or link.endswith('.png') or link.endswith('.gif'):
                    print('link found')
                    await ctx.send('loading revue starlight shitpost')
                    # Read quotes from file
                    with open('quotes.txt') as f:
                        quotes = f.read().splitlines()

                    # Get a random quote
                    random_quote = random.choice(quotes)

                    # Download the image/gif from the link
                    response = requests.get(link)
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    if image.format == 'GIF':
                        await ctx.send('the given image is a gif, may take a while')

                    # Create the captioned image/gif
                    caption = f'{random_quote.strip()}'
                    image_with_caption = await create_image_with_caption(image, caption)

                    # Send the captioned image/gif
                    await ctx.send(file=image_with_caption)
                    return
                elif link.startswith('https://tenor.com'):
                    print('tenor link found')
                    # Get the GIF URL from the Tenor link
                    response = requests.get(link)
                    if response.ok and "json" in response.headers["content-type"]:
                        gif_url = response.json()["url"]
                        # Do something with the GIF URL
                    else:
                        print("Invalid response")

                    # Download the GIF
                    gif_content = requests.get(gif_url).content

                    # Convert the GIF content to an imageio-readable format
                    gif_bytes = bytearray(gif_content)

                    # Read the GIF using imageio
                    gif_image = imageio.imread(gif_bytes, "gif")

                    # Save the GIF to a file
                    imageio.mimsave("tenor.gif", [gif_image])

                    await ctx.send('loading revue starlight shitpost')
                    # Read quotes from file
                    with open('quotes.txt') as f:
                        quotes = f.read().splitlines()

                    # Get a random quote
                    random_quote = random.choice(quotes)

                    # Download the image/gif from the link
                    response = requests.get(gif_image)
                    image_data = gif_content
                    image = gif_image
                    if image.format == 'GIF':
                        await ctx.send('the given image is a gif, may take a while')

                    # Create the captioned image/gif
                    caption = f'{random_quote.strip()}'
                    image_with_caption = await create_image_with_caption(image, caption)

                    # Send the captioned image/gif
                    await ctx.send(file=image_with_caption)
                    
    else:
        attachment = ctx.message.attachments[0]
        if attachment.content_type.startswith('image/') or attachment.content_type.startswith('video/'):
            await ctx.send('loading revue starlight shitpost')
            # Read quotes from file
            with open('quotes.txt') as f:
                quotes = f.read().splitlines()

            # Get a random quote
            random_quote = random.choice(quotes)

            # Read the image/gif file
            image_data = await attachment.read()
            image = Image.open(io.BytesIO(image_data))
            if image.format == 'GIF':
                await ctx.send('the given image is a gif, may take a while')

            # Create the captioned image/gif
            caption = f'{random_quote.strip()}'
            image_with_caption = await create_image_with_caption(image, caption)

            # Send the captioned image/gif
            await ctx.send(file=image_with_caption)
            return

    # If no attachment is found in the most recent message, send an error message
    await ctx.send('Please attach an image or gif to caption')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if random.random() < 0.05:  # 5% chance of replying
        with open('qotd.txt', encoding='utf-8') as f:
            quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

        # Get a random quote
        await message.reply(random.choice(quotes))
        # Process any commands in the message
        await bot.process_commands(message)
    else:
        # Process any commands in the message
        await bot.process_commands(message)
        return

async def create_image_with_caption(image, caption, max_width_ratio=0.3):
    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Get the width and height of the image/gif
    width, height = image.size

    # Set the font and size
    font = ImageFont.truetype('impact.ttf', int(height / 15))

    # Calculate the maximum width of the caption text
    max_text_width = int(width * 0.08)

    # Wrap the caption text to fit within the maximum width
    wrapped_caption = textwrap.wrap(caption, width=max_text_width)

    # Calculate the size of the wrapped caption text
    text_width, text_height = draw.textsize('\n'.join(wrapped_caption), font=font)

    # Calculate the position of the caption text
    x = (width - text_width) / 2
    y = height - (text_height * 2)

    frames = []
    # Loop through all frames of the gif and add the caption text to each frame
    try:
        while True:
            image.seek(len(frames))
            frame = Image.new('RGB', (width, height + (text_height * (len(wrapped_caption) + 1))), color='white')
            frame.paste(image, (0, text_height * (len(wrapped_caption) + 1)))
            frame_draw = ImageDraw.Draw(frame)
            frame_draw.text((x, 0), '\n'.join(wrapped_caption), font=font, fill='black')
            frames.append(frame)
    except EOFError:
        pass

    # Save the captioned gif to a buffer and return it as a Discord file
    if len(frames) == 1:
        buf = io.BytesIO()
        frames[0].save(buf, 'PNG')
    else:
        buf = io.BytesIO()
        frames[0].save(buf, format='GIF', save_all=True, append_images=frames[1:], duration=image.info['duration'], loop=0)
    buf.seek(0)

    return discord.File(buf, filename='captioned.gif' if image.format == 'GIF' else 'captioned.png')

bot.run(TOKEN)