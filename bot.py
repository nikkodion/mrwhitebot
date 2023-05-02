import os

import discord
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
from dotenv import load_dotenv
from discord.ext import commands, tasks
import random
import requests
import imageio
import json
import textwrap
import nltk.corpus
from maincog import MainCog
import asyncio
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TENOR_TOKEN = os.getenv('TENOR_TOKEN')

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

reactions = [] # list to store available reactions

async def setup(bot):
    await bot.add_cog(MainCog(bot))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await setup(bot)
    update_reactions.start() # start background task to update reactions
    bot.loop.create_task(schedule_image())

@bot.command(name='t')
async def tcall(ctx):
    main_cog = bot.get_cog("MainCog")
    await main_cog.tspeak(ctx)

@bot.command(name='commands')
async def helpcommands(ctx):
    with open('commands.txt') as f:
        textcommands = f.read()
    await ctx.send(textcommands)

bot.remove_command('help')

@bot.command(name='help')
async def helpcommands1(ctx):
    with open('commands.txt') as f:
        textcommands = f.read()
    await ctx.send(textcommands)

@bot.command(name='quote')
async def quote(ctx):
    with open('qotd.txt', encoding='utf-8') as f:
        quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

    # Get a random quote
    await ctx.send(random.choice(quotes))
    

@bot.command(name='gif')
async def revuegif(ctx):

    apikey = TENOR_TOKEN 
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
    apikey = TENOR_TOKEN 
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
    apikey = TENOR_TOKEN 
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
    apikey = TENOR_TOKEN 
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
    if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                if attachment.content_type.startswith('image/'):
                    image_data = await attachment.read()
                    loadingmessage = await ctx.send('loading mr white image')
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
                    await loadingmessage.delete()
    else:
        await ctx.send('please include an image to mr whiteify')


@bot.command(name='shitpostchar')
async def revueshitpostchar(ctx):
    # set the apikey and limit
    apikey = TENOR_TOKEN 
    lmt = 1
    ckey = "mrwhitebot" 

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

        # Check if the file size exceeds the maximum allowed size
        with io.BytesIO() as buffer:
            image.save(buffer, format='GIF')
            file_size = len(buffer.getvalue())
        if file_size > 8000000:  # 8 MB in bytes
            # Open the image using PIL
            image = Image.open(image.filename)

            # Reduce the image size by half
            new_size = (int(image.size[0] * 0.5), int(image.size[1] * 0.5))
            image = image.resize(new_size, Image.ANTIALIAS)

            # Reduce the image quality to 70%
            image.save(image.filename, optimize=True, quality=70)
        else:
            # Create the captioned image/gif
            caption = f'{random_quote.strip()}'
            image_with_caption = await create_image_with_caption(image, caption)
            if image_with_caption.filename == 'captioned.png':
                await ctx.send("File was too large, try again [1]")
                await loadingmessage.delete()
                return
            try:
                await ctx.send(file=image_with_caption)
                await loadingmessage.delete()
            except discord.errors.HTTPException as error:
                await ctx.send("File was too large, try again [2]")
        return
    else:
        top_8gifs = None

@bot.command(name='shitpost')
async def revueshitpostquote(ctx):
    # set the apikey and limit
    apikey = TENOR_TOKEN 
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

        # Check if the file size exceeds the maximum allowed size
        with io.BytesIO() as buffer:
            image.save(buffer, format='GIF')
            file_size = len(buffer.getvalue())
        if file_size > 8000000:  # 8 MB in bytes
            # Open the image using PIL
            image = Image.open(image.filename)

            # Reduce the image size by half
            new_size = (int(image.size[0] * 0.5), int(image.size[1] * 0.5))
            image = image.resize(new_size, Image.ANTIALIAS)

            # Reduce the image quality to 50%
            image.save(image.filename, optimize=True, quality=50)
            print('image quality successfully reduced')
        else:
            # Create the captioned image/gif
            caption = f'{random_quote.strip()}'
            image_with_caption = await create_image_with_caption(image, caption)
            if image_with_caption.filename == 'captioned.png':
                await ctx.send("File was too large, try again [1]")
                await loadingmessage.delete()
                return
            try:
                await ctx.send(file=image_with_caption)
            except discord.errors.HTTPException as error:
                await ctx.send("File was too large, try again [2]")

        await loadingmessage.delete()
        return
    
@bot.command(name='sticker')
async def relivesticker(ctx):
    png_url = get_random_png_url()
    await ctx.send(png_url)

@bot.command(name='bday')
async def relivebday(ctx):
    text, file = get_random_bday_voice()
    await ctx.send(text, file=file)

@bot.command(name='voice')
async def relivevoice(ctx):
    text, file = get_random_voice()
    await ctx.send(text, file=file)

@tasks.loop(hours=24)
async def update_reactions():
    guild = bot.get_guild(593878082654568458)
    if guild:
        emojis = await guild.fetch_emojis()
        global reactions
        reactions = [emoji for emoji in emojis if emoji.animated == False]
    


@update_reactions.before_loop
async def before_update_reactions():
    await bot.wait_until_ready() # wait until the bot is ready

@bot.command(name='kys')
async def kyscall(ctx):
    # Get a list of all the files in the "talking" folder
    files = os.listdir('talking')
    
    # Filter the list to only include files that start with "newkys"
    newkys_files = [f for f in files if f.startswith('newkys')]
    
    if len(newkys_files) == 0:
        # No files starting with "newkys" were found in the folder
        await ctx.send("No kys files found.")
        return
    
    # Select a random file from the "newkys" files
    selected_file = random.choice(newkys_files)
    
    # Send the file as a message
    with open(f"talking/{selected_file}", "rb") as f:
        file = discord.File(f)
        await ctx.send(file=file)


@bot.command(name='delete')
async def deleteserver(ctx):
    if str(ctx.author) == 'EX Falchion#8379':
        confirmation_msg = await ctx.send("Are you sure you want to delete the ENTIRE server?\nPlease reply Y/N")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['y', 'n']
        try:
            response_msg = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await confirmation_msg.edit(content="Confirmation timed out.")
            return
        if response_msg.content.lower() == 'y':
            return
        else:
            await ctx.send("The server will not be deleted.")
    else:
        await ctx.send("You do not have permission to do this.")

# Define a dictionary to store the rate for each server
server_rates = {}

@bot.command(name='rate')
async def ratecall(ctx):
    # Get the rate for the current server from the dictionary, or use a default value of 0.01
    rate = server_rates.get(ctx.guild.id, 0.0015)
    rate_percent = rate * 100
    overall_rate_percent = (1 - ((1 - rate)**5)) * 100
    await ctx.send("There is currently a {}% chance of each type of reply, and a {}% chance of any kind of reply overall!".format(rate_percent, overall_rate_percent))

@bot.command(name='setrate')
@commands.has_permissions(administrator=True)
async def setratecall(ctx, rate: float):
    # Update the rate for the current server in the dictionary
    server_rates[ctx.guild.id] = rate
    rate_percent = rate * 100
    overall_rate_percent = (1 - ((1 - rate)**5)) * 100
    await ctx.send("Reply rate for each type of reply updated to {}% for this server! ({}% overall!)".format(rate_percent, overall_rate_percent))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    rate = server_rates.get(message.guild.id, 0.0015) # get server rate, if none than default .15%

    if random.random() < rate: # default .15% chance of replying with a quote
        with open('qotd.txt', encoding='utf-8') as f:
            quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

        # Get a random quote
        await message.reply(random.choice(quotes))

    if random.random() < rate: # default .15% chance of replying
        folder = 'talking'
        images = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]
        if images:
            await message.reply(file=discord.File(random.choice(images)))
        else:
            await message.reply("No images found.")
    
    if 'white' in message.content.lower():
        await message.channel.send("https://i.ibb.co/vzQZ9yz/hikariwhitesmall.png")
    
    if 'for now' in message.content.lower() and random.random() < 0.5: # 50% chance to reply with junna if "for now" in message
        file_path = os.path.join(os.getcwd(), 'talking', 'newjunna.png')
        file = discord.File(file_path)
        await message.channel.send(file=file)
    
    if random.random() < rate: # default .15% chance of reacting
        if reactions:
            reaction = random.choice(reactions)
            try:
                await message.add_reaction(reaction)
            except:
                pass
        else:
            await message.reply("tried to send reaction but none found")
    
    if random.random() < rate: # default .15% chance of replying with a sticker
        png_url = get_random_png_url()
        await message.reply(png_url)
    
    if random.random() < rate: # default .15% chance of replying with a voice line
        text, file = get_random_voice()
        await message.reply(text, file=file)
    await bot.process_commands(message)



def get_random_png_url():
    png_endpoint = 'https://cdn.karth.top/api/assets/ww/res_en/res/item_root/medium'
    response = requests.get(png_endpoint)
    png_list = response.json()['response_data']

    filenames = [png['filename'] for png in png_list if png['type'] == 'image']

    random_filename = random.choice(filenames)

    png_url = f'https://cdn.karth.top/api/assets/ww/res_en/res/item_root/medium/{random_filename}'

    return png_url



def get_random_bday_voice():
    random_number = random.randint(101, 109)
    random_numberstr = str(random_number)
    voices = f'https://cdn.karth.top/api/assets/jp/res/sound/voice/{random_numberstr}'
    voicesresponse = requests.get(voices)
    wav_list = voicesresponse.json()['response_data']
    filenames = [wav['filename'] for wav in wav_list if wav['type'] == 'audio']
    random_filename = random.choice(filenames)
    voice_url = f'https://cdn.karth.top/api/assets/jp/res/sound/voice/{random_number}/{random_filename}'

    character = "default"
    if random_number == 101: character = "Karen"
    elif random_number == 102: character = "Hikari"
    elif random_number == 103: character = "Mahiru"
    elif random_number == 104: character = "Claudine"
    elif random_number == 105: character = "Maya"
    elif random_number == 106: character = "Junna"
    elif random_number == 107: character = "Nana"
    elif random_number == 108: character = "Futaba"
    elif random_number == 109: character = "Kaoruko"

    character1 = character + " would like to say something:\n"
    character2 = character + " has this to say:\n"
    character3 = character + " has a message:\n"

    characterw = random.choice([character1, character2, character3])

    response = requests.get(voice_url)
    file = discord.File(io.BytesIO(response.content), filename='message.wav')

    return characterw, file

def get_random_voice():
    advjson = 'https://karth.top/api/adventure.json'
    advresponse = requests.get(advjson)
    advdata = advresponse.json()
    ids = []  # Initialize an empty list to store the ids

    for key in advdata['main_story'].keys():
        ids.append(advdata['main_story'][key]['id'])

    random_event = random.choice(ids)
    reventjson = f'https://cdn.karth.top/api/assets/dlc/res/scenario/voice/{random_event}'
    reventresponse = requests.get(reventjson)
    reventdata = reventresponse.json()

    filenames = [item['filename'] for item in reventdata['response_data'] if item['type'] == 'audio' and item['filename'].endswith('.wav')]

    random_filename = random.choice(filenames)

    voice_url = f'https://cdn.karth.top/api/assets/dlc/res/scenario/voice/{random_event}/{random_filename}'

    response = requests.get(voice_url)
    file = discord.File(io.BytesIO(response.content), filename='message.wav')

    m1 = "Hold on, why don't you listen to what this character has to say:\n"
    m2 = "This character has this to say about that:\n"
    m3 = "Wait, let this character say their opinion:\n"
    m4 = "That's really interesting, but have you considered:\n"
    m5 = "About that. We just received this message from Seisho Music Academy:\n"
    m6 = "Hmm, OK. But what if I were to get a Revue Starlight character to say this:\n"

    characterw = random.choice([m1, m2, m3, m4, m5, m6])

    return characterw, file


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

    file_size = len(buf.getvalue())

    if file_size > 8000000:  # 8 MB in bytes
        return discord.File(buf, filename='captioned.png')

    return discord.File(buf, filename='captioned.gif' if image.format == 'GIF' else 'captioned.png')



async def send_gm_image(channel_ids):
    apikey = TENOR_TOKEN 
    lmt = 2
    ckey = "mrwhitebot"

    search_term = "revue starlight good morning"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_2gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_2gifs['results']]
        random_url = random.choice(gif_urls)
        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            await channel.send("It's 10AM!\n" + random_url)
    else:
        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            await channel.send("It's 10AM!\n" + "there was an error but good morning anyway")

async def send_ga_image(channel_ids):
    apikey = TENOR_TOKEN 
    lmt = 2
    ckey = "mrwhitebot"

    search_term = "revue starlight good afternoon"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_2gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_2gifs['results']]
        random_url = random.choice(gif_urls)
        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            await channel.send("It's 2PM!\n" + random_url)
    else:
        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            await channel.send("It's 2PM!\n" + "there was an error but good afternoon anyway")

async def send_gn_image(channel_ids):
    apikey = TENOR_TOKEN 
    lmt = 2
    ckey = "mrwhitebot"

    search_term = "revue starlight good night"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_2gifs = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_2gifs['results']]
        random_url = random.choice(gif_urls)
        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            await channel.send("It's 10PM!\n" + random_url)
    else:
        for channel_id in channel_ids:
            channel = bot.get_channel(channel_id)
            await channel.send("It's 10PM!\n" + "there was an error but good night anyway")

async def schedule_image():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
        if now.hour == 10 and now.minute == 0 and now.second == 0:
            await send_gm_image([593878082654568460, 545321213858414603])
        elif now.hour == 14 and now.minute == 0 and now.second == 0:
            await send_ga_image([593878082654568460, 545321213858414603])
        elif now.hour == 22 and now.minute == 0 and now.second == 0:
            await send_gn_image([593878082654568460, 545321213858414603])
        await asyncio.sleep(1)

bot.run(TOKEN)