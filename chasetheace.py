import random
import models
from collections import Counter
from multiprocessing import Pool

class Strategy:
	def __init__(self):
		self.strategy = []
	def shouldswap(self, players, position, card, previousCard):
		if card > previousCard:
			return False
		if card > 7:
			return False
		return True

rand = random.SystemRandom()


playercount = 10
#Randomly generate x players
players = []
playernames = models.getPlayerNames()

for p in range(0,playercount):
	strat = Strategy()
	players.append(models.Player(strat,playernames.pop()))

def run(num):
	loses = dict()
	runs = 1000000
	for x in range(0,runs):
		if x % (runs/1000) == 0:
			print "Num "+str(num)+ " "+str((x*100.0)/runs) + "%"
		remaining = models.playRound(players)
		for remain in remaining:
			index = players.index(remain)
			if index in loses:
				loses[index] += 1
			else:
				loses[index] = 1
	return loses
results = []
pool = Pool()
loses = Counter()
for x in range(0,10):
	results.append(pool.apply_async(run,[x]))
for result in results:
	loses = loses + Counter(result.get())
print "Loses at end is "
print loses



