import settings
import discord

from discord import Client
from scoring import Board
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
client = Client()

REACTIONS = ['\N{THUMBS UP SIGN}', '\N{THUMBS DOWN SIGN}']


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if not message.content.startswith('!'):
        return
    
    channel_id = message.channel.id
    board = Board(channel_id)
    tokens = message.content.split()
    
    # Add a member to the list
    if tokens[0] == '!add':
        name_id = message.mentions[0].id
        board.add_member(name_id)
        await message.channel.send('ok')
        
    # Ask for voting
    elif tokens[0] == '!score':
        
        # Retrieve data
        _, name, score, *commit = tokens
        score = int(score)
        name_id = message.mentions[0].id
        
        board.add_score(name_id, score)
        
        if len(commit) == 0:
            commit = ['For no reason']
        
        # Construct output
        prefix = '+' if score > 0 else ''
        text = f'''> {message.author.mention} => <@{name_id}> {prefix}{score}
                   > {' '.join(commit)}'''
                   
        message_sent = await message.channel.send(text)
    
        for emoji in REACTIONS: 
            await message_sent.add_reaction(emoji)
    
    # Display graph (horizontal bar chart)
    elif tokens[0] == '!show':
        
        messages = await message.channel.history(limit=200).flatten()
        await message.channel.send(list(messages))
                
        all_members = {user.id: user.name for user in bot.get_all_members()}
        await message.channel.send(all_members)
        
        pic_path = board.get_summary_pic(all_members)
        picture = discord.File(pic_path)
        await message.channel.send(file=picture)
    
    # Display graph (historical line chart)
    elif tokens[0] == '!timeline':
        pic_path = board.get_timeline()
        picture = discord.File(pic_path)
        await message.channel.send(file=picture)
    
@bot.event
async def on_raw_reaction_add(payload):
    """
    Remove reactions other than thumbs up and down
    """
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

    if message.author.id == bot.user.id and payload.emoji.name not in REACTIONS:
        await reaction.remove(payload.member)



bot.run(settings.DISCORD_TOKEN)
