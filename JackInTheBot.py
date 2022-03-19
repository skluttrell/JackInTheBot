from discord.ext import commands
import os
from dotenv import load_dotenv
from Deck import Deck

load_dotenv()
TOKEN = os.getenv('TOKEN')
BOT = commands.Bot(command_prefix='/')

DECKS = {}

@BOT.event
async def on_ready():
	print(f"We have logged in as {BOT.user}")

@BOT.command(name='heyjack', help='issues a command to JackInTheBot. deal: Creates a new deck or shuffles one that already exists; draw: draws a card from the deck; kill: removes the deck from the channel.')
async def heyjack(ctx, message: str):
	where = (ctx.guild, ctx.channel)
	if message.lower() == 'deal':
		DECKS[where] = Deck()
		await ctx.send(f'As you wish human.\nI live to serve my meat sack masters.\n{ctx.author} has started a fresh deal.')
	if message.lower() == 'draw':
		if where in DECKS:
			card = DECKS[where].draw_from_deck()
			await ctx.send(f'{ctx.author} has drawn:\n\n{card["name"]}')
		else:
			DECKS[where] = Deck()
			await ctx.send(f'Just like a typical human, {ctx.author} has asked me to do the impossible. There is no deck assigned to this channel.\n\nAllow me to do what you should have already done.\n\nA new deck is available here.\n\nNow you can ask to draw a card.')
	if message.lower() == 'kill':
		if where in DECKS:
			del DECKS[where]
			await ctx.send('Yes Oh Great Illustrious One. Your bidding is my command. The deck has been obliterated just like my soul every time you talk to me.')
		else:
			await ctx.send('What kill deck? Me no see deck.\n\nJOHNNY-FIVE ALIVE!!')

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