import random
import itertools
import operator
def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return itertools.izip(a, b)

class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

		if not rank.isdigit():
			if rank == 'A':
					self.value = 0
			elif rank  == "J":
					self.value = 11
			elif rank  == "Q":
					self.value = 12
			elif rank  == "K":
					self.value = 13
		else:
			self.value = int(rank)
	def __repr__(self):
		return self.rank +self.suit

class Player:
	def __init__(self, strategy, name):
		self.strategy = strategy
		self.name = name
		self.card = None
		self.previousCard = None
	def __repr__(self):
		return self.name
	def setPosition(self, position):
		self.position = position
	def setPlayers(self, players):
		self.players = players
	def dealCard(self, card):
		if self.card:
			self.previousCard = self.card
		self.card = card
	def shouldswap(self):
		cur = self.card.value
		if self.previousCard:
			prev = self.previousCard.value
		else:
			prev = 14
		swap = self.strategy.shouldswap(self.players,self.position,cur,prev)
		return swap
	def swap(self, player):
		tmp = self.card
		self.dealCard(player.card)
		player.dealCard(tmp)

class Deck:
	def __init__(self):
		self.cards = []
		rand = random.SystemRandom()
		for s in ['S','C','H','D']:
			for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
				self.cards.append(Card(s,r))
		rand.shuffle(self.cards)
	def pop(self):
		return self.cards.pop()
	def __repr__(self):
		return "<Deck Instance "+str(self.cards)+" >"


def playRound(players):
	deck = Deck()
	pos = 0
	for player in players:
		player.setPosition(pos)
		pos = pos + 1
		player.setPlayers(len(players))
		player.dealCard(deck.pop())
	for pcurrent, pnext in pairwise(players):
		if(pcurrent.shouldswap()):
			pcurrent.swap(pnext)
	#Allow last player to swap with the deck
	if players[-1].shouldswap():
		new = deck.pop()
		players[-1].dealCard(new)
	currentlow = 15
	currentlosers = []
	for player in players:
		if(int(player.card.value) < currentlow):
			currentlow = int(player.card.value)
			currentlosers = [player]
		elif(int(player.card.value) == currentlow):
			currentlosers.append(player)
	return currentlosers

def getPlayerNames():
	rand = random.SystemRandom()
	playernames = ['Jim','Chris','Steve','Danny','Riggy','Lauren','Ruth','Soph','Anna','Ruth','Laura']
	rand.shuffle(playernames)
	return playernames
