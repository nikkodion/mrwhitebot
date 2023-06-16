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

# get the environment variables from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TENOR_TOKEN = os.getenv('TENOR_TOKEN')

# make sure discord intents all enabled
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True
intents.guild_messages = True

# create bot with command prefix of ! and intents
bot = commands.Bot(command_prefix='!', intents=intents)

reactions = [] # list to store available reactions

async def setup(bot):
    """
    Adds MainCog from maincog.py to bot, which has the "tspeak" function.
    Necessary to be in an async def function, so that bot.add_cog() can be awaited.
    This function is called in the on_ready() function below.

    Args:
        bot (commands.Bot()): the Discord bot
    """
    await bot.add_cog(MainCog(bot))

server_rates = {} # list to store server rates

@bot.event
async def on_ready():
    """
    Automatically runs when the bot goes online.
    Prints to console to know when it has connected to Discord,
    adds the cog, updates reactions, schedules timed messages,
    and loads the server rates from the json.
    """
    print(f'{bot.user.name} has connected to Discord!') # generic print statement to know it's online
    await setup(bot) # call setup method above to add cog

    # start background task to update reactions
    update_reactions.start()

    # schedule good morning, good afternoon, good night messages
    bot.loop.create_task(schedule_image()) 

    # load server rates from json file into list (so that it doesn't reset when bot goes offline)
    global server_rates
    with open('server_rates.json', 'r') as f:
        server_rates = json.load(f)

# !t: replies to replied to message with a speech bubble image (method in cog)
@bot.command(name='t')
async def tcall(ctx):
    """
    Triggers upon !t command, which, on user reply to a message, the bot
    replies to that message with a Revue Starlight frame with a speech bubble

    Args:
        ctx (context): "context" containing info about command message
    """
    # get an instance of the cog and call the function in it
    main_cog = bot.get_cog("MainCog")
    await main_cog.tspeak(ctx)

# !commands: sends info from commands.txt
@bot.command(name='commands')
async def helpcommands(ctx):
    """
    Triggers upon !commands command, sends a message containing the
    bot commands, stored in commands.txt

    Args:
        ctx (context): "context" containing info about command message
    """
    with open('commands.txt') as f:
        textcommands = f.read()
    await ctx.send(textcommands)

# !help: removes default help command and replaces with custom (same function as above)
bot.remove_command('help')

@bot.command(name='help')
async def helpcommands1(ctx):
    """
    Triggers upon !help command, sends a message containing the
    bot commands, stored in commands.txt

    Args:
        ctx (context): "context" containing info about command message
    """
    with open('commands.txt') as f:
        textcommands = f.read()
    await ctx.send(textcommands)

# !quote: gets a quote from 'qotd.txt' and send it
@bot.command(name='quote')
async def quote(ctx):
    """
    Triggers upon !quote command, sends a random quote from the Revue
    Starlight movie, from qotd.txt

    Args:
        ctx (context): "context" containing info about command message
    """
    # need to open as utf-8
    with open('qotd.txt', encoding='utf-8') as f:
        quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

    # Get a random quote
    await ctx.send(random.choice(quotes))
    
# !gif: sends a random gif from tenor under the search term "revue starlight"
@bot.command(name='gif')
async def revuegif(ctx):
    """
    Triggers upon !gif command, sends a random gif using Tenor API
    from the keywords "revue starlight"

    Args:
        ctx (context): "context" containing info about command message
    """

    apikey = TENOR_TOKEN 
    lmt = 1
    ckey = "mrwhitebot" 

    search_term = "revue starlight"

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s&random=true" % (search_term, apikey, ckey,  lmt))

    if r.status_code == 200:
        top_gif = json.loads(r.content)
        gif_urls = [gif['url'] for gif in top_gif['results']]
        await ctx.send("\n".join(gif_urls))
    else:
        top_gif = None

@bot.command(name='gm')
async def good_morning(ctx):
    """
    Triggers upon !gm command, sends a random gif using Tenor API
    from the keywords "revue starlight good morning"

    Args:
        ctx (context): "context" containing info about command message
    """
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
    """
    Triggers upon !ga command, sends a random gif using Tenor API
    from the keywords "revue starlight good afternoon"

    Args:
        ctx (context): "context" containing info about command message
    """
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
    """
    Triggers upon !gn command, sends a random gif using Tenor API
    from the keywords "revue starlight good night"

    Args:
        ctx (context): "context" containing info about command message
    """

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
    """
    Triggers upon !mrwhite command, if the message has an image, it tries
    to use OpenCV to detect faces and uses PIL to open that image and
    put mrwhiteface.png where there are faces.

    Args:
        ctx (context): "context" containing info about command message
    """
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
    """
    Triggers upon !shitpostchar command, sends a random gif using Tenor API
    and then captions it using PIL with a random character from Revue
    Starlight from quotes.txt

    Args:
        ctx (context): "context" containing info about command message
    """
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
        top_gif = json.loads(r.content)
        with open('quotes.txt') as f:
            quotes = f.read().splitlines()

        # Get a random quote
        random_quote = random.choice(quotes)

        loadingmessage = await ctx.send("loading randomly generated revue starlight shitpost")

        # Read the image/gif file
        all_formats= [gif['media_formats'] for gif in top_gif['results']]
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
        top_gif = None

@bot.command(name='shitpost')
async def revueshitpostquote(ctx):
    """
    Triggers upon !shitpost command, sends a random gif using Tenor API
    and then captions it using PIL with a random quote from the Revue
    Starlight movie from qotd.txt

    Args:
        ctx (context): "context" containing info about command message
    """
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
        top_gif = json.loads(r.content)

        with open('qotd.txt', encoding='utf-8') as f:
            quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

        # Get a random quote
        random_quote = random.choice(quotes)

        loadingmessage = await ctx.send("loading randomly generated revue starlight shitpost")

        # Read the image/gif file
        all_formats= [gif['media_formats'] for gif in top_gif['results']]
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
    
@bot.command(name='captionchar')
async def captionrevuechar(ctx):
    """
    Triggers upon !captionchar, if the message has an image or a replied-to message
    has an image, it sends quotes.txt to captiongivenmessage,
    which handles captioning the image with a Revue Starlight character

    Args:
        ctx (context): "context" containing info about command message
    """
    await captiongivenmessage(ctx, 'quotes.txt')

@bot.command(name='caption')
async def captionrevue(ctx):
    """
    Triggers upon !caption, if the message has an image or a replied-to message
    has an image, it sends qotd.txt to captiongivenmessage,
    which handles captioning the image with a quote from the Revue Starlight movie

    Args:
        ctx (context): "context" containing info about command message
    """
    await captiongivenmessage(ctx, 'qotd.txt')

async def captiongivenmessage(ctx, txtfile):
    """
    Called by !captionchar and !caption, if the message has an image or a replied-to message
    has an image, it uses the given text file to caption the image with PIL

    Args:
        ctx (context): "context" containing info about command message
        txtfile (text file): text file containing either the character names or Revue Starlight movie quotes
    """
    if not ctx.message.attachments and not ctx.message.content.startswith('http'): # check if the current message has no attachments or link
        replied_to = ctx.message.reference and ctx.message.reference.resolved # if no attachments, check the replied to message
        if replied_to: # first check that replied to message exists
            if replied_to.attachments or replied_to.content.startswith('http'): # if the replied to message has attachment or link
                message = replied_to # then make the message to edit the replied message
            else:
                await ctx.send("Please either attach an image or reply to a message with an attached image")
        else: # if still the replied to message doesn't have an attachment or link
            await ctx.send("Please either attach an image or reply to a message with an attached image")
            return
    else: # if the current message has attachments or link,
        message = ctx.message # then make the message to edit the message itself

    if message.attachments: # check if the message has an attachment
        attachment = message.attachments[0] # set attachment to the first attachment
        if attachment.content_type.startswith('image/'): # or attachment.content_type.startswith('video/'): if the attachment is an image
            loadingmessage = await ctx.send("loading randomly generated revue starlight shitpost") # send a loading message

            # read lines from text file (qotd.txt needs special treatment)
            if txtfile == 'qotd.txt':
                with open('qotd.txt', encoding='utf-8') as f:
                    quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]
            else:
                with open(txtfile) as f:
                    quotes = f.read().splitlines()

            random_quote = random.choice(quotes) # get a random line from text file

            # read the image/gif file
            image_data = await attachment.read()
            image = Image.open(io.BytesIO(image_data))

            # create the captioned gif (don't need to check file size because discord already does for attached images)
            caption = f'{random_quote.strip()}'
            image_with_caption = await create_image_with_caption(image, caption)

            # send the captioned gif
            await ctx.send(file=image_with_caption)
            await loadingmessage.delete() # delete loading message
            await ctx.send(f"(!caption used by {ctx.author.name})")
            await ctx.message.delete()
            return
    elif message.content.startswith('http'): # if the message has no attachment, then check if it has a link
        link = message.content.strip() # take link
        if link.endswith('.jpg') or link.endswith('.jpeg') or link.endswith('.png') or link.endswith('.gif'): # check if its already a direct link
            print(link)
            loadingmessage = await ctx.send('loading randomly generated revue starlight shitpost') #if so, start loading

            # read lines from text file (qotd.txt needs special treatment)
            if txtfile == 'qotd.txt':
                with open('qotd.txt', encoding='utf-8') as f:
                    quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]
            else:
                with open(txtfile) as f:
                    quotes = f.read().splitlines()

            random_quote = random.choice(quotes) # get a random line from text file

            # download the image/gif from the link
            response = requests.get(link)
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))

            if link.endswith('.gif'): # if the link was a gif
                # check if the file size exceeds the maximum allowed size
                with io.BytesIO() as buffer:
                    image.save(buffer, format='GIF')
                    file_size = len(buffer.getvalue())
                if file_size > 8000000:  # 8 MB in bytes
                    # open the image using PIL
                    image = Image.open(image.filename)

                    # reduce the image size by half
                    new_size = (int(image.size[0] * 0.5), int(image.size[1] * 0.5))
                    image = image.resize(new_size, Image.ANTIALIAS)

                    # reduce the image quality to 70%
                    image.save(image.filename, optimize=True, quality=70)
                else:
                    # create the captioned gif
                    caption = f'{random_quote.strip()}'
                    image_with_caption = await create_image_with_caption(image, caption)
                    if image_with_caption.filename == 'captioned.png':
                        await ctx.send("File was too large, try again [1]")
                        await loadingmessage.delete()
                        return
                    try:
                        await ctx.send(file=image_with_caption)
                        await loadingmessage.delete()
                        await ctx.send(f"(!caption used by {ctx.author.name})")
                        await ctx.message.delete()
                    except discord.errors.HTTPException as error:
                        await ctx.send("File was too large, try again [2]")
                    return   
            else:
                # create the captioned image
                caption = f'{random_quote.strip()}'
                image_with_caption = await create_image_with_caption(image, caption)

                # send the captioned image
                await ctx.send(file=image_with_caption)
                await loadingmessage.delete() # delete loading message
                await ctx.send(f"(!caption used by {ctx.author.name})")
                await ctx.message.delete()
                return  
        elif link.startswith('https://tenor.com'): # check if a tenor link instead of direct
            # set the apikey
            apikey = TENOR_TOKEN 
            ckey = "mrwhitebot"
            gifid = link.split("-")[-1] # get the gif id from the tenor link

            # request the link from the api
            r = requests.get("https://tenor.googleapis.com/v2/posts?key=%s&ids=%s&ckey=%s&media_filter=gif" % (apikey, gifid, ckey))

            if r.status_code == 200: # if successful

                # read lines from text file (qotd.txt needs special treatment)
                if txtfile == 'qotd.txt':
                    with open('qotd.txt', encoding='utf-8') as f:
                        quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]
                else:
                    with open(txtfile) as f:
                        quotes = f.read().splitlines()

                random_quote = random.choice(quotes) # get a random line from text file

                loadingmessage = await ctx.send("loading randomly generated revue starlight shitpost") # send loading message

                # get the direct image url from the json
                r_data = r.json()
                url = r_data['results'][0]['media_formats']['gif']['url']
                image_data = requests.get(url)
                    
                # open the url
                image = Image.open(io.BytesIO(image_data.content))

                # check if the file size exceeds the maximum allowed size
                with io.BytesIO() as buffer:
                    image.save(buffer, format='GIF')
                    file_size = len(buffer.getvalue())
                if file_size > 8000000:  # 8 MB in bytes
                    # open the image using PIL
                    image = Image.open(image.filename)

                    # reduce the image size by half
                    new_size = (int(image.size[0] * 0.5), int(image.size[1] * 0.5))
                    image = image.resize(new_size, Image.ANTIALIAS)

                    # reduce the image quality to 70%
                    image.save(image.filename, optimize=True, quality=70)
                else:
                    # create the captioned gif
                    caption = f'{random_quote.strip()}'
                    image_with_caption = await create_image_with_caption(image, caption)
                    if image_with_caption.filename == 'captioned.png':
                        await ctx.send("File was too large, try again [1]")
                        await loadingmessage.delete()
                        return
                    try:
                        await ctx.send(file=image_with_caption)
                        await loadingmessage.delete()
                        await ctx.send(f"(!caption used by {ctx.author.name})")
                        await ctx.message.delete()
                    except discord.errors.HTTPException as error:
                        await ctx.send("File was too large, try again [2]")
                    return    

    
@bot.command(name='sticker')
async def relivesticker(ctx):
    """
    Triggers upon !sticker, sends a random sticker from Revue Starlight
    Re LIVE using Karthuria API

    Args:
        ctx (context): "context" containing info about command message
    """
    png_url = get_random_png_url()
    if ctx.message.reference:
        replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
        await replied_message.reply(png_url)
        await ctx.send(f"(!sticker used by {ctx.author.name})")
        await ctx.message.delete()
    else:
        await ctx.send(png_url)

@bot.command(name='bday')
async def relivebday(ctx):
    """
    Triggers upon !bday, sends a birthday voice line from Revue Starlight
    Re LIVE using Karthuria API

    Args:
        ctx (context): "context" containing info about command message
    """
    text, file = get_random_bday_voice()
    await ctx.send(text, file=file)

@bot.command(name='voice')
async def relivevoice(ctx):
    """
    Triggers upon !voice, sends a random voice line from Revue Starlight
    Re LIVE story mode using Karthuria API

    Args:
        ctx (context): "context" containing info about command message
    """
    text, file = get_random_voice()
    if ctx.message.reference:
        replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
        await replied_message.reply(text, file=file)
        await ctx.send(f"(!voice used by {ctx.author.name})")
        await ctx.message.delete()    
    else:
        await ctx.send(text, file=file)

@tasks.loop(hours=24)
async def update_reactions():
    """
    Task that updates emotes the bot can react with every 24 hours
    """
    guild = bot.get_guild(593878082654568458)
    if guild:
        emojis = await guild.fetch_emojis()
        global reactions
        reactions = [emoji for emoji in emojis if emoji.animated == False]
    


@update_reactions.before_loop
async def before_update_reactions():
    """
    Waits until the bot is ready before updating reactions
    """
    await bot.wait_until_ready()

@bot.command(name='delete')
async def deleteserver(ctx):
    """
    Triggers upon !delete, joke method that only works if EX Falchion

    Args:
        ctx (context): "context" containing info about command message
    """
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

@bot.command(name='rate')
async def ratecall(ctx):
    """
    Triggers upon !rate, sends the current rate for a random message

    Args:
        ctx (context): "context" containing info about command message
    """
    # Get the rate for the current server from server_rates.json, or use a default value of 0.01
    if str(ctx.guild.id) in server_rates:
        rate = server_rates[str(ctx.guild.id)]
    else:
        rate = 0.001  # Default rate
    rate_percent = rate * 100
    overall_rate_percent = (1 - ((1 - rate)**5)) * 100
    await ctx.send("There is currently a {}% chance of each type of reply, and a {:.2f}% chance of any kind of reply overall!".format(rate_percent, overall_rate_percent))

@bot.command(name='setrate')
@commands.has_permissions(administrator=True)
async def setratecall(ctx, rate: float):
    """
    Triggers upon !setrate, sets the current rate for a random message

    Args:
        ctx (context): "context" containing info about command message
    """
    # Update the rate for the current server in server_rates.json
    global server_rates
    server_rates[str(ctx.guild.id)] = rate
    with open('server_rates.json', 'w') as f:
        json.dump(server_rates, f)
    rate_percent = rate * 100
    overall_rate_percent = (1 - ((1 - rate)**5)) * 100
    await ctx.send("Reply rate for each type of reply updated to {}% for this server! ({:.2f}% overall!)".format(rate_percent, overall_rate_percent))

@bot.event
async def on_message(message):
    """
    Triggers upon any message by a user in the server, handling all random
    replies and any special prompts such as "white" and "for now"

    Args:
        message: the message that was most recently sent
    """
    if message.author == bot.user:
        return
    
    if bot.user in message.mentions or message.reference and message.reference.resolved.author == bot.user:
        if not message.content.startswith('!'):
            random_number = random.randint(1, 3)
            if random_number == 1:
                with open('qotd.txt', encoding='utf-8') as f:
                    quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

                # Get a random quote
                await message.reply(random.choice(quotes))
            elif random_number == 2:
                png_url = get_random_png_url()
                await message.reply(png_url)
            elif random_number == 3:
                text, file = get_random_voice()
                await message.reply(text, file=file)

    for guild in bot.guilds:
        if guild.id == message.guild.id:
            if str(guild.id) in str(server_rates):
                rate = server_rates[str(guild.id)]
            else:
                rate = 0.001  # get server rate, if none than default .1%
            break

    if random.random() < rate: # default .1% chance of replying with a quote
        with open('qotd.txt', encoding='utf-8') as f:
            quotes = [line.rsplit(",,", 1)[-1] for line in f.readlines()]

        # Get a random quote
        await message.reply(random.choice(quotes))

    if random.random() < rate: # default .1% chance of replying
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
    
    if random.random() < rate: # default .1% chance of reacting
        if reactions:
            reaction = random.choice(reactions)
            try:
                await message.add_reaction(reaction)
            except:
                pass
        else:
            await message.reply("tried to send reaction but none found")
    
    if random.random() < rate: # default .1% chance of replying with a sticker
        png_url = get_random_png_url()
        await message.reply(png_url)
    
    if random.random() < rate: # default .1% chance of replying with a voice line
        text, file = get_random_voice()
        await message.reply(text, file=file)
    await bot.process_commands(message)



def get_random_png_url():
    """
    Helper method called when using !sticker to take Karthuria endpoint and send
    URL of a random sticker
    """
    png_endpoint = 'https://cdn.karth.top/api/assets/ww/res_en/res/item_root/medium'
    response = requests.get(png_endpoint)
    png_list = response.json()['response_data']

    filenames = [png['filename'] for png in png_list if png['type'] == 'image']

    random_filename = random.choice(filenames)

    png_url = f'https://cdn.karth.top/api/assets/ww/res_en/res/item_root/medium/{random_filename}'

    return png_url



def get_random_bday_voice():
    """
    Helper method called when using !bday to take Karthuria endpoint and send
    URL of a random bday voice line
    """
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

    character1 = character + " would like to congratulate you on your birthday:\n"
    character2 = character + " has this to say about your birthday:\n"
    character3 = character + " has a birthday message:\n"

    characterw = random.choice([character1, character2, character3])

    response = requests.get(voice_url)
    file = discord.File(io.BytesIO(response.content), filename='message.wav')

    return characterw, file

def get_random_voice():
    """
    Helper method called when using !voice to take Karthuria endpoint and send
    URL of a random voice line
    """
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
    """
    Helper method called to edit images for any methods that need it
    """
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

    if (text_height > 50):
        frame_height = height + (text_height//2 * (len(wrapped_caption) + 1))
    else:
        frame_height = height + (text_height * (len(wrapped_caption) + 1))

    frames = []
    # Loop through all frames of the gif and add the caption text to each frame
    try:
        while True:
            image.seek(len(frames))
            frame = Image.new('RGB', (width, frame_height), color='white')
            if (text_height > 50):
                frame.paste(image, (0, text_height//2 * (len(wrapped_caption) + 1)))
            else:
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
    """
    Helper method called to use Tenor API to find good morning message
    """
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
    """
    Helper method called to use Tenor API to find good afternoon message
    """
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
    """
    Helper method called to use Tenor API to find good night message
    """
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
    """
    Method that schedules and sends the gm, ga, and gn messages
    """
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