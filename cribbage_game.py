#Cribbage

import random, copy
import numpy.random
from statistics import mean
import itertools
import matplotlib.pyplot as plt

class Card:
	#Represents a standard playing card

	#Suit Mapping:
		# H --> 0
		# S --> 1
		# D --> 2
		# C --> 3
	#Rank Mapping:
		# A --> 1
		# J --> 11
		# Q --> 12
		# K --> 13
		# 2-10 map to their values

	SUITS = ["H", "S", "D", "C"]	#Heart, Spade, Diamond, Club
	RANKS = [None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
	VALUES = [None, 1, 2, 3, 4,  5, 6, 7, 8, 9, 10, 10, 10, 10]

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.value = self.VALUES[rank]

	def __str__(self):
		return "[%s, %s]" % (Card.RANKS[self.rank],
							 Card.SUITS[self.suit])

	def __eq__(self, card):
		#Compares rank and suit
		#Needed to get the index of the correct card
		if self.rank == card.rank and self.suit == card.suit:
			return 1
		else:
			return 0

	def __ne__(self, card):
		if self == card:
			return 0
		else:
			return 1

	# def __lt__(self, card):
	# 	if self.rank < card.rank:
	# 		return 1
	# 	else:
	# 		return 0

	# def __le__(self, card):
	# 	if self.rank < card.rank or self.rank == card.rank:
	# 		return 1
	# 	else:
	# 		return 0

	# def __gt__(self, card):
	# 	if self.rank > card.rank:
	# 		return 1
	# 	else:
	# 		return 0

	# def __ge__(self, card):
	# 	if self.rank > card.rank or self.rank == card.rank:
	# 		return 1
	# 	else:
	# 		return 0

class Deck:
	#Represents a standard 52 card deck

	def __init__(self):
		self.cards = []
		for suit in range(4):
			for rank in range(1, 14):
				card = Card(rank, suit)
				self.cards.append(card)

	def __str__(self):
		res = [str(card) for card in self.cards]
		return ", ".join(res)

	def __len__(self):
		return len(self.cards)
	
	def pop_card(self):
		#Remove a card from the deck and return it
		return self.cards.pop()

	def add_card(self, card):
		#Adds a card to the deck
		self.cards.append(card)

	def shuffle(self):
		#Randomize the deck (shuffle it)
		random.shuffle(self.cards)

	def sort(self):
		#Sort the cards in ascending order
		for i in range(1, len(self)):
			val = self.cards[i]
			j = i - 1
			while (j >= 0) and (self.cards[j].rank > val.rank):
				self.cards[j+1] = self.cards[j]
				j = j - 1
			self.cards[j+1] = val
		return self

	def deal_hand(self, hand1):
		#Deals 6 cards to 1 player
		for i in range(6):
			hand1.add_card(self.pop_card())

	def deal_hands(self, hand1, hand2):
		#Deals 6 cards to 2 players
		for i in range(6):
			hand1.add_card(self.pop_card())
			hand2.add_card(self.pop_card())

def card_list_equal(l1, l2):
	#Determine if two lists of cards are equal
	if len(l1) != len(l2):
		return 0
	else:
		for i in range(len(l1)):
			if l1[i] != l2[i]:
				return 0
	return 1

def print_card_list(card_list):
	for card in card_list:
		print card

class Hand(Deck):
	#Represents a hand of playing cards
	#Inherents from Deck, so we can use pop_card and add_card for Hands

	def __init__(self, label=''):
		self.cards = []
		self.label = label

	def equals(self, hand):
		count = 0
		for card_i in self.cards:
			for card_j in hand.cards:
				if card_i == card_j:
					count += 1
		if count == 6:
			return True
		else:
			return False

	def clear_hand(self):
		self.cards = []

	def remove_card(self, hand, index):
		#Removes card at given index and places in a different hand
		#For use when discarding into crib
		#Example:  player_hand = [A, D] [A, C] [2, D] [3, S] [6, H] [7, S]
		#		   player_hand.remove_card(crib, 4)
		#		   player_hand = [A, D] [A, C] [2, D] [3, S] [7, S]
		#		   crib = [6, H]
		hand.add_card(self.cards.pop(index))

	def get_pairs(self):
		#Return a list of all the pairs in hand
		#Only works on sorted list of cards
		pairs = []
		hand_size = len(self)
		for card_i in self.cards:
			index_j = self.cards.index(card_i) + 1
			if index_j < hand_size:
				for card_j in self.cards[index_j:]:
					if card_j.rank == card_i.rank:
						pairs.append([card_i, card_j])
					elif card_j.rank > card_i.rank:
						break
		return pairs

	def get_fifteens(self):
		#Return a list of all fifteens in hand
		#Checks up to 5 cards since you will have max 5 cards during scoring
		fifteens = []
		hand_size = len(self)
		for card_i in self.cards:
			index_j = self.cards.index(card_i) + 1
			if index_j < hand_size:
				for card_j in self.cards[index_j:]:
					sum_cards = card_i.value + card_j.value
					if sum_cards == 15:
						fifteens.append([card_i, card_j])
					elif sum_cards < 15:
						index_k = self.cards.index(card_j) + 1
						if index_k < hand_size:
							for card_k in self.cards[index_k:]:
								sum_cards = card_i.value + card_j.value + card_k.value
								if sum_cards == 15:
									fifteens.append([card_i, card_j, card_k])
								elif sum_cards < 15:
									index_m = self.cards.index(card_k) + 1
									if index_m < hand_size:
										for card_m in self.cards[index_m:]:
											sum_cards = card_i.value + card_j.value + card_k.value + card_m.value
											if sum_cards == 15:
												fifteens.append([card_i, card_j, card_k, card_m])
											elif sum_cards < 15:
												index_n = self.cards.index(card_m) + 1
												if index_n < hand_size:
													for card_n in self.cards[index_n:]:
														sum_cards = card_i.value + card_j.value + card_k.value + card_m.value + card_n.value
														if sum_cards == 15:
															fifteens.append([card_i, card_j, card_k, card_m, card_n])
		return fifteens

	def drop_duplicates(self):
		#Return list of cards without duplicates
		#Given hand must be sorted
		no_duplicates = []
		seen = set()
		for card_i in self.cards:
			if card_i.rank not in seen:
				seen.add(card_i.rank)
				no_duplicates.append(card_i)
		return no_duplicates

	def get_duplicates(self):
		#Return a list of duplicate cards, i.e those not contained in drop_duplicates
		#Given hand must be sorted
		duplicates = []
		seen = set()
		for card_i in self.cards:
			if card_i.rank not in seen:
				seen.add(card_i.rank)
			else:
				duplicates.append(card_i)
		return duplicates

	def get_all_no_duplicates(self):
		all_no_dup = []
		duplicates = self.get_duplicates()
		no_duplicates = self.drop_duplicates()
		if not duplicates:
			new_no_dup = copy.deepcopy(no_duplicates)
			all_no_dup.append(new_no_dup)
			return all_no_dup
		else:
			i = 1
			while i == 1:
				for no_dup in all_no_dup:
					if card_list_equal(no_dup, no_duplicates):
						i = 0
				new_no_dup = copy.deepcopy(no_duplicates)
				all_no_dup.append(new_no_dup)
				card = duplicates.pop(0)
				for card_i in no_duplicates:
					if card.rank == card_i.rank:
						duplicates.append(card_i)
						index_i = no_duplicates.index(card_i)
						no_duplicates[index_i] = card
			return all_no_dup[:(len(all_no_dup)-1)]


	def get_runs(self):
		#Return a list of all runs in hand
		#Runs are a sequence of 3 or more
		runs = []
		all_no_dup = self.get_all_no_duplicates()
		for no_duplicates in all_no_dup:
			possible_run = []
			num_no_duplicates = len(no_duplicates)
			for i in range(num_no_duplicates):
				if not possible_run:
					possible_run.append(no_duplicates[i])
				else:
					length = len(possible_run)
					if no_duplicates[i].rank == (possible_run[length-1].rank + 1):
						possible_run.append(no_duplicates[i])
						if i == (num_no_duplicates - 1) and len(possible_run) >= 3:
							# print "Possible Run"
							# print_card_list(possible_run)
							j = 1
							for r in runs:
								if card_list_equal(possible_run, r):
									j = 0
							if j == 1:
								runs.append(possible_run)
					else: 
						if len(possible_run) >= 3:
							# print "Possible Run"
							# print_card_list(possible_run)
							j = 1
							for r in runs:
								if card_list_equal(possible_run, r):
									j = 0
							if j == 1:
								runs.append(possible_run)
						possible_run = []
						possible_run.append(no_duplicates[i])
		return runs

	def get_score(self):
		#Return score sum from fifteens, runs, pairs
		score = 0
		fifteens = self.get_fifteens()
		runs = self.get_runs()
		pairs = self.get_pairs()

		# #Get score for fifteens
		# for fifteen in fifteens:
		# 	print_card_list(fifteen)
		fifteen_score = 2*len(fifteens)
		# print fifteen_score
		#Get score for runs
		# for run in runs:
		# 	print_card_list(run)
		runs_score = 0
		for run in runs:
			runs_score += len(run)
		# print runs_score
		#Get score for pairs
		# for pair in pairs:
		# 	print_card_list(pair)
		pair_score = 2*len(pairs)
		# print pair_score

		score = fifteen_score + runs_score + pair_score

		return score

def create_population(n):
	population = set([])	#List of hands
	for i in range(n):
		#Create deck
		deck = Deck()
		deck.shuffle()
		#Create hand
		hand = Hand()
		deck.deal_hand(hand)
		hand.sort()
		while hand in population:
			#Create deck
			deck = Deck()
			deck.shuffle()
			#Create hand
			hand = Hand()
			deck.deal_hand(hand)
			hand.sort()
		population.add(hand)
	population = list(population)
	return population

def assign_values(n):
	hand_values = []
	for j in range(n):
		value = []
		for i in range(6):
			rand_num = random.random()
			while rand_num < .1 or rand_num > .9:
				rand_num = random.random()
			value.append(rand_num)
		hand_values.append(value)
	return hand_values

def optimal_score(hand):
	# print "HAND"
	# print hand
	opt_score = 0
	for i in range(5):
		#print "i = ", i
		for j in range(i+1, 6):
			#print "j = ", j
			test_hand = Hand()
			test_hand.cards = copy.deepcopy(hand.cards)
			crib = Hand()
			test_hand.remove_card(crib, i)
			test_hand.remove_card(crib, j-1)
			# print "==================================="
			# print "TEST HAND"
			# print test_hand
			#Assume your crib
			#test_score = test_hand.get_score() + crib.get_score()
			#Assume opponent's crib
			test_score = test_hand.get_score() - crib.get_score()
			# print test_score
			# print "==================================="
			if test_score > opt_score:
				opt_score = test_score
	#print "\n"
	return opt_score

def discard(hand, crib, possible_hands, values):
	rank_list = []
	for card in hand.cards:
		rank_list.append(card.rank)
	rank_list.sort()
	#print "RANK LIST: ", rank_list
	#rank_array = numpy.array([rank_list])
	#print possible_hands.shape
	index = -1
	for i in range(possible_hands.shape[0]):
		h = list(possible_hands[i])
		h.sort()
		if h == rank_list:
			index = i
	value = list(values[i])
	index_min1 = value.index(min(value))
	min1 = value.pop(index_min1)
	index_min2 = value.index(min(value))
	min2 = value.pop(index_min2)
	hand.remove_card(crib, index_min1)
	hand.remove_card(crib, index_min2)
		# counter = 0
		# for rh in hand:
		# 	for r in rank_list:
		# 		if rh == r:
		# 			counter += 1
		# 			#print counter
		# 		if counter == 6:
		# 			print possible_hands[i]
		# 			break



def main():

	print "\n\n"

	#Get possible hands
	possible_hands = numpy.loadtxt('hands.txt', delimiter=",")
	values_opponent = numpy.loadtxt('values_opponent.txt', delimiter=",")
	values_computer = numpy.loadtxt('values_computer.txt', delimiter=",")

	#Randomly choose who deals first, player or computer
	#	If 0, computer goes first.  If 0, player goes first.
	whose_deal = random.randint(0, 1)
	if whose_deal:
		print "Player deals first"
	else:
		print "Computer deals first"

	score_player = 0
	score_computer = 0

	# deck = Deck()
	# deck.shuffle()
	# hand_player = Hand("Player's Hand")
	# hand_computer = Hand("Computer's Hand")
	# crib = Hand("Crib")
	# deck.deal_hands(hand_computer, hand_player)
	# discard(hand_computer, crib, possible_hands, values_opponent)
	# print "HAND"
	# for card in hand_computer.cards:
	# 	print card
	# print "CRIB"
	# for card in crib.cards:
	# 	print card

	num_points_to_win = 25

	while score_player < num_points_to_win and score_computer < num_points_to_win:
		deck = Deck()
		deck.shuffle()
		hand_player = Hand("Player's Hand")
		hand_computer = Hand("Computer's Hand")
		crib = Hand("Crib")

		if whose_deal:
			print "\nPLAYER'S DEAL\n"
			deck.deal_hands(hand_computer, hand_player)
			flip_card = deck.pop_card()
			i = 0
			for card in hand_player.cards:
				print i, ": ", card
				i += 1
			index1 = int(raw_input("Choose first card to discard: "))
			print "\n"
			hand_player.remove_card(crib, index1)
			i = 0
			for card in hand_player.cards:
				print i, ": ", card
				i += 1
			index2 = int(raw_input("Choose second card to discard: "))
			hand_player.remove_card(crib, index2)

			print "\nFlip Card: "
			print flip_card

			discard(hand_computer, crib, possible_hands, values_opponent)
			
			print "\n"
			print "Computer's Hand: "
			for card in hand_computer.cards:
				print card

			hand_computer.add_card(flip_card)
			score_computer += hand_computer.get_score()
			print "\nComputer's points (hand): ", hand_computer.get_score()
			print "Computer's total score: ", score_computer
			if score_computer >= num_points_to_win:
				print 'COMPUTER WINS!'

			print "\nPlayer's Hand"
			for card in hand_player.cards:
				print card
			hand_player.add_card(flip_card)
			crib.add_card(flip_card)
			score_player += hand_player.get_score()
			score_player += crib.get_score()
			
			print "\nPlayer's points (hand): ", hand_player.get_score()
			print "Player's points (crib): ", crib.get_score()
			print "Player's total score: ", score_player
			if score_player >= num_points_to_win and score_computer < num_points_to_win:
				print 'PLAYER WINS!'

			whose_deal = 0
		else:
			print "\nCOMPUTER'S DEAL\n"
			deck.deal_hands(hand_player, hand_computer)
			i = 0
			for card in hand_player.cards:
				print i, ": ", card
				i += 1
			print "\n"
			index1 = int(raw_input("Choose first card to discard: "))
			hand_player.remove_card(crib, index1)
			i = 0
			for card in hand_player.cards:
				print i, ": ", card
				i += 1
			print "\n"
			index2 = int(raw_input("Choose second card to discard: "))
			hand_player.remove_card(crib, index2)

			flip_card = deck.pop_card()
			print "\nFlip Card: "
			print flip_card

			discard(hand_computer, crib, possible_hands, values_computer)
			hand_player.add_card(flip_card)
			score_player += hand_player.get_score()
			print "\n"
			print "Player's Hand: "
			for card in hand_player.cards:
				print card
			print "\nPlayer's points (hand): ", hand_player.get_score()
			print "Player's total score: ", score_player
			if score_player >= num_points_to_win:
				print 'PLAYER WINS!'
			print "\n"
			print "Computer's Hand: "
			for card in hand_computer.cards:
				print card
			hand_computer.add_card(flip_card)
			crib.add_card(flip_card)
			score_computer += hand_computer.get_score()
			score_computer += crib.get_score()
			print "\nComputer's points (hand): ", hand_computer.get_score()
			print "Computer's points (crib): ", crib.get_score()
			print "Computer's total score: ", score_computer
			if score_computer >= num_points_to_win and score_player < num_points_to_win:
				print 'COMPUTER WINS!'
			whose_deal = 1


	

	

if __name__ == '__main__':
	main()