from rdoclient import RandomOrgClient
from dotenv import load_dotenv
import random
import os
import logging

load_dotenv()
RDO_KEY = os.getenv('RDO_KEY')
logging.basicConfig(format='%(asctime)s %(message)s', filename='fallback.log', level=logging.DEBUG)

class Deck:
	def __init__(self):
		self._CARDTYPES = [
			{ 'name': 'Ace of Spades', 'value': (1,11) },
			{ 'name': 'Two of Spades', 'value': (2) },
			{ 'name': 'Three of Spades', 'value': (3) },
			{ 'name': 'Four of Spades', 'value': (4) },
			{ 'name': 'Five of Spades', 'value': (5) },
			{ 'name': 'Six of Spades', 'value': (6) },
			{ 'name': 'Seven of Spades', 'value': (7) },
			{ 'name': 'Eight of Spades', 'value': (8) },
			{ 'name': 'Nine of Spades', 'value': (9) },
			{ 'name': 'Ten of Spades', 'value': (10) },
			{ 'name': 'Jack of Spades', 'value': (10) },
			{ 'name': 'Queen of Spades', 'value': (10) },
			{ 'name': 'King of Spades', 'value': (10) },
			{ 'name': 'Ace of Clubs', 'value': (1,11) },
			{ 'name': 'Two of Clubs', 'value': (2) },
			{ 'name': 'Three of Clubs', 'value': (3) },
			{ 'name': 'Four of Clubs', 'value': (4) },
			{ 'name': 'Five of Clubs', 'value': (5) },
			{ 'name': 'Six of Clubs', 'value': (6) },
			{ 'name': 'Seven of Clubs', 'value': (7) },
			{ 'name': 'Eight of Clubs', 'value': (8) },
			{ 'name': 'Nine of Clubs', 'value': (9) },
			{ 'name': 'Ten of Clubs', 'value': (10) },
			{ 'name': 'Jack of Clubs', 'value': (10) },
			{ 'name': 'Queen of Clubs', 'value': (10) },
			{ 'name': 'King of Clubs', 'value': (10) },
			{ 'name': 'Ace of Hearts', 'value': (1,11) },
			{ 'name': 'Two of Hearts', 'value': (2) },
			{ 'name': 'Three of Hearts', 'value': (3) },
			{ 'name': 'Four of Hearts', 'value': (4) },
			{ 'name': 'Five of Hearts', 'value': (5) },
			{ 'name': 'Six of Hearts', 'value': (6) },
			{ 'name': 'Seven of Hearts', 'value': (7) },
			{ 'name': 'Eight of Hearts', 'value': (8) },
			{ 'name': 'Nine of Hearts', 'value': (9) },
			{ 'name': 'Ten of Hearts', 'value': (10) },
			{ 'name': 'Jack of Hearts', 'value': (10) },
			{ 'name': 'Queen of Hearts', 'value': (10) },
			{ 'name': 'King of Hearts', 'value': (10) },
			{ 'name': 'Ace of Diamonds', 'value': (1,11) },
			{ 'name': 'Two of Diamonds', 'value': (2) },
			{ 'name': 'Three of Diamonds', 'value': (3) },
			{ 'name': 'Four of Diamonds', 'value': (4) },
			{ 'name': 'Five of Diamonds', 'value': (5) },
			{ 'name': 'Six of Diamonds', 'value': (6) },
			{ 'name': 'Seven of Diamonds', 'value': (7) },
			{ 'name': 'Eight of Diamonds', 'value': (8) },
			{ 'name': 'Nine of Diamonds', 'value': (9) },
			{ 'name': 'Ten of Diamonds', 'value': (10) },
			{ 'name': 'Jack of Diamonds', 'value': (10) },
			{ 'name': 'Queen of Diamonds', 'value': (10) },
			{ 'name': 'King of Diamonds', 'value': (10) },
		]
		self._cards: list = []
		self._discard_pile: list = []
		self._reveal21 = False
		self.deal()

	def deal(self):
		""" Creates a new deck """
		max = len(self._CARDTYPES) - 1
		client = RandomOrgClient(RDO_KEY)
		try:
			# Generate a list of random card numbers from random.org
			self._cards = client.generate_integers(max+1, 0, max, False)
		except Exception as e:
			logging.exception(e)
			# Fallback to Python's pseudo random generrator
			self._cards = [ i for i in range(0,52) ]
			random.shuffle(self._cards)

	def draw_from_deck(self) -> dict:
		""" Draws a new card """
		if self._cards:
			card = self._CARDTYPES[self._cards[0]]
			self._cards.pop(0)
			return card
		return False

	def draw_from_pile(self) -> dict:
		""" Pull the top card from the discard pile """
		if self._discard_pile:
			idx = len(self._discard_pile) - 1
			card = self._CARDTYPES[self._discard_pile[idx]]
			self._discard_pile.pop(idx)
			return card
		return False

	def discard_card(self, card: dict):
		""" Place a card from the user's hand to the discard pile """
		self._discard_pile.append(card)

	@property
	def cards_remaining(self) -> int:
		""" Returns the number of cards left in the deck """
		return len(self._cards)

	@property
	def Number_of_discarded_cards(self) -> int:
		""" Returns the number of cards in the discard pile """
		return len(self._discard_pile)

	@property
	def top_card(self) -> dict:
		""" Returns the topmost card visible on the discard pile """
		if self._discard_pile:
			return self._discard_pile[len(self._discard_pile)-1]
		return False

	@property
	def reveal21(self) -> bool:
		"""
			Returns the state of the boolean
			that allows a user to view the revealed
			card in a game of 21
		"""
		return self._reveal21

	@reveal21.setter
	def reveal21(self, value: bool):
		""" Sets the reveal21 bool """
		self._reveal21 = value

# Dec:
# Has a cards pile and a discard pile
# Shuffle: puts all the cards into the deck and shuffles them
# admins can: reshuffle a deck
# Users can see: the number of cards in both piles, the top card of the discard pile
# Users can: draw a card from the deck or discard pile
# Admins can set: rather or not users can see the first card in each of their hands (for 21)
# Hand:
# Belongs to specific user
# users can: draw from deck, place card on discard pile, see their hand (DM), see the number of cards in their hand (DM), ?value of their hand?, see another user's exposed card for 21,  pass cards to other players

if __name__ == '__main__':
	test = Deck()
	for _ in range(0,52):
		card = test.draw_from_deck()
		print(card['name'])