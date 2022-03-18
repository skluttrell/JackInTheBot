from discord.ext import commands
import os
from dotenv import load_dotenv
from Deck import Deck

load_dotenv()
TOKEN = os.getenv('TOKEN')
BOT = commands.Bot(command_prefix='/')


decks = {}

@BOT.event
async def on_ready():
	print(f"We have logged in as {BOT.user}")

@BOT.command(name='heyjack', help='Issues a command to JackInTheBot')
async def heyjack(ctx, com: str):
	await ctx.send(f'Server: {ctx.guild}; channel: {ctx.channel}; author: {ctx.author}')

@BOT.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send('You do not have the correct role for this command.')

@BOT.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as outF:
		if event == 'on_message':
			outF.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

BOT.run(TOKEN)


# Creats a deck for the channel
# The deck has a deck of cards and a discard pile
# users can draw a card from the deck into their hand and place that card from their hand to the discard pile
# Users can invoke the bot to a channel which creates the deck for that channel
# Who ever invites the bot has reshuffle permissions and cann administrate the deck
# users must be in that channel to effect the channel's deck
# Each user has their own hand
# Dismissing the bot destroys the deck for that channel