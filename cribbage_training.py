#Train the computer for each hand

import random, copy
import numpy.random
from statistics import mean
import itertools
import matplotlib.pyplot as plt

#Rank Mapping:
# A --> 1
# J --> 11
# Q --> 12
# K --> 13
# 2-10 map to their values

RANKS = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 
			6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 
			10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 
			13, 13, 13, 13]
VALUES = {1:1, 2:2, 3:3, 4:4,  5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 
			11:10, 12:10, 13:10}

POSSIBLE_HANDS = itertools.combinations(RANKS, 6)
POSSIBLE_HANDS = set([c for c in POSSIBLE_HANDS])
POSSIBLE_HANDS = list(POSSIBLE_HANDS)
NUM_HANDS = len(POSSIBLE_HANDS)

def write_trained_results(filename, hands, values):
	path = 'C:\Python27\\' + filename + '.txt'
	f = open(path, 'w')
	for value in values:
		for v in value:
			f.write("%.17f, " % v)
		f.write("\n")
	num_hands = len(hands)

def read_trained_results(filename):
	path = 'C:\Python27\\' + filename + '.txt'

def get_pairs(hand):
	#Return a list of all the pairs in hand
	#Only works on sorted list of cards
	pairs = []
	hand_size = len(hand)
	for i in range(hand_size):
		j = i + 1
		if j < hand_size:
			card_i = hand[i]
			for card_j in hand[j:]:
				if card_j == card_i:
					pairs.append([card_i, card_j])
				elif card_j > card_i:
					break
	return pairs

def get_fifteens(hand):
	#Return a list of all fifteens in hand
	#Checks up to 5 cards since you will have max 5 cards during scoring
	fifteens = []
	hand_size = len(hand)
	for i in range(hand_size):
		card_i = hand[i]
		if (i+1) < hand_size:
			for j in range((i+1), hand_size):
				card_j = hand[j]
				sum_cards = VALUES[card_i] + VALUES[card_j]
				if sum_cards == 15:
					fifteens.append([card_i, card_j])
				elif sum_cards < 15:
					if (j+1) < hand_size:
						for k in range((j+1), hand_size):
							card_k = hand[k]
							sum_cards = VALUES[card_i] + VALUES[card_j] + VALUES[card_k]
							if sum_cards == 15:
								fifteens.append([card_i, card_j, card_k])
							elif sum_cards < 15:
								if (k+1) < hand_size:
									for m in range((k+1), hand_size):
										card_m = hand[m]
										sum_cards = VALUES[card_i] + VALUES[card_j] + VALUES[card_k] + VALUES[card_m]
										if sum_cards == 15:
											fifteens.append([card_i, card_j, card_k, card_m])
										elif sum_cards < 15:
											if (m+1) < hand_size:
												for n in range((m+1), hand_size):
													card_n = hand[n]
													sum_cards = VALUES[card_i] + VALUES[card_j] + VALUES[card_k] + VALUES[card_m] + VALUES[card_n]
													if sum_cards == 15:
														fifteens.append([card_i, card_j, card_k, card_m, card_n])
	return fifteens

def drop_duplicates(hand):
	#Return list of cards without duplicates
	#Given hand must be sorted
	no_duplicates = []
	seen = set()
	for card_i in hand:
		if card_i not in seen:
			seen.add(card_i)
			no_duplicates.append(card_i)
	return no_duplicates

def get_duplicates(hand):
	#Return a list of duplicate cards, i.e those not contained in drop_duplicates
	#Given hand must be sorted
	duplicates = []
	seen = set()
	for card_i in hand:
		if card_i not in seen:
			seen.add(card_i)
		else:
			duplicates.append(card_i)
	return duplicates

def get_all_no_duplicates(hand):
	all_no_dup = []
	duplicates = get_duplicates(hand)
	j = .11
	for d in range(len(duplicates)):
		duplicates[d] += j
		j += .01
	#print "LIST OF DUPLICATES: ", duplicates
	no_duplicates = drop_duplicates(hand)
	k = .21
	for n in range(len(no_duplicates)):
		no_duplicates[n] += k
		k += .01
	#print "LIST WITHOUT DUPLICATES: ", no_duplicates
	if not duplicates:
		new_no_dup = copy.deepcopy(no_duplicates)
		all_no_dup.append(new_no_dup)
		for n in range(len(all_no_dup)):
			no_dup = all_no_dup[n]
			for m in range(len(no_dup)):
				all_no_dup[n][m] = int(all_no_dup[n][m])
		return all_no_dup
	else:
		i = 1
		while i == 1:
			for no_dup in all_no_dup:
				if no_dup == no_duplicates:
					i = 0
			new_no_dup = copy.deepcopy(no_duplicates)
			all_no_dup.append(new_no_dup)
			card = duplicates.pop(0)
			card_t = int(card)
			for card_i in no_duplicates:
				card_i_t = int(card_i)
				if card_t == card_i_t:
					duplicates.append(card_i)
					index_i = no_duplicates.index(card_i)
					no_duplicates[index_i] = card
		for n in range(len(all_no_dup)):
			no_dup = all_no_dup[n]
			for m in range(len(no_dup)):
				all_no_dup[n][m] = int(all_no_dup[n][m])
		return all_no_dup[:(len(all_no_dup)-1)]

def get_runs(hand):
	#Return a list of all runs in hand
	#Runs are a sequence of 3 or more
	runs = []
	all_no_dup = get_all_no_duplicates(hand)
	#print "LISTS OF NO DUPLICATES: ", all_no_dup
	for no_duplicates in all_no_dup:
		possible_run = []
		num_no_duplicates = len(no_duplicates)
		for i in range(num_no_duplicates):
			if not possible_run:
				possible_run.append(no_duplicates[i])
			else:
				length = len(possible_run)
				if no_duplicates[i] == (possible_run[length-1] + 1):
					possible_run.append(no_duplicates[i])
					if i == (num_no_duplicates - 1) and len(possible_run) >= 3:
						# print "Possible Run"
						# print_card_list(possible_run)
						j = 1
						runs.append(possible_run)
						# for r in runs:
						# 	if possible_run == r:
						# 		j = 0
						# if j == 1:
						# 	runs.append(possible_run)
				else: 
					if len(possible_run) >= 3:
						# print "Possible Run"
						# print_card_list(possible_run)
						j = 1
						runs.append(possible_run)
						# for r in runs:
						# 	if possible_run == r:
						# 		j = 0
						# if j == 1:
						# 	runs.append(possible_run)
					possible_run = []
					possible_run.append(no_duplicates[i])
	return runs

def get_score(hand):
	#Return score sum from fifteens, runs, pairs
	score = 0
	fifteens = get_fifteens(hand)
	runs = get_runs(hand)
	pairs = get_pairs(hand)
	#Get score for fifteens
	fifteen_score = 2*len(fifteens)
	#Get score for runs
	runs_score = 0
	for run in runs:
		runs_score += len(run)
	#Get score for pairs
	pair_score = 2*len(pairs)
	#Total score
	score = fifteen_score + runs_score + pair_score
	return score

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

def optimal_score(hand, player):
	# print "HAND"
	# print hand
	opt_score = 0
	for i in range(5):
		#print "i = ", i
		for j in range(i+1, 6):
			#print "j = ", j
			test_hand = []
			test_hand = copy.deepcopy(hand)
			crib = []
			crib.append(test_hand.pop(i))
			crib.append(test_hand.pop(j-1))
			crib.sort()
			# print "==================================="
			# print "TEST HAND"
			# print test_hand
			if player == "computer":
				test_score = get_score(test_hand) + get_score(crib)
			else:
				test_score = get_score(test_hand) - get_score(crib)
			#test_score = get_score(test_hand) 
			# print test_score
			# print "==================================="
			if test_score > opt_score:
				opt_score = test_score
	#print "\n"
	return opt_score

def plot_averages(avg_scores):
	plt.plot(avg_scores)
	plt.ylabel("Average Score")
	plt.show()

def create_population(n=NUM_HANDS):
	if n == NUM_HANDS:
		return POSSIBLE_HANDS
	else:
		population = []
		rang = range(NUM_HANDS)
		# print rang[:n]
		random.shuffle(rang)
		# print rang[:n]
		hand_indices = rang[:n]
		for i in hand_indices:
			population.append(POSSIBLE_HANDS[i])
		# print population
		return population


def train_player(n=NUM_HANDS, m=400):

	population = create_population(n)
	hand_values = assign_values(n)

	players = ["computer", "opponent"]
	for player in players:

		print player

		optimal_scores = []
		
		for i in range(n):
			hand = population[i]
			hand = list(hand)
			# print hand
			# print hand_values[i]
			# print "\n"
			opt_score = optimal_score(hand, player)
			optimal_scores.append(opt_score)

		optimal_average = mean(optimal_scores)
		print "OPTIMAL AVERAGE: " , optimal_average
		print "\n"

		population_crib = []
		scores = []
		avg_scores = []

		for j in range(m):
			for i in range(n):
				#Get minimum values
				value = copy.deepcopy(hand_values[i])
				index_min1 = value.index(min(value))
				min1 = value.pop(index_min1)
				#print "index_min1 = ", index_min1
				index_min2 = value.index(min(value))
				min2 = value.pop(index_min2)
				#print "index_min2 = ", index_min2
				#Get card to throw
				crib = []
				hand = copy.deepcopy(population[i])
				hand = list(hand)
				crib.append(hand.pop(index_min1))
				crib.append(hand.pop(index_min2))
				crib.sort()
				population_crib.append(crib)
				if player == 'computer':
					score = get_score(hand) + get_score(crib)
				else:
					score = get_score(hand) - get_score(crib)
				#score = get_score(hand)
				scores.append(score)
				#print "SCORE: ", score
				opt_score = optimal_scores[i]
				#print "OPTIMAL SCORE: ", opt_score
				if score < (0.75*opt_score):
					#print "UNSUCCESSFUL"
					new_value1 = random.random()
					while new_value1 < .1 or new_value1 > .9:
						new_value1 = random.random()
					new_value2 = random.random()
					while new_value2 < .1 or new_value2 > .9:
						new_value2 = random.random()
					hand_values[i][index_min1] = new_value1
					hand_values[i][index_min2] = new_value2
				# print "UPDATED VALUES", hand_values[i]
				# print "\n"
					# gaussian_number1 = numpy.random.normal(min1, 0.1)
					# gaussian_number2 = numpy.random.normal(min2, 0.1)
					# print "min1 = ", min1
					# print "gaussian_number1 = ", gaussian_number1
					# print "min2 = ", min2
					# print "gaussian_number2 = ", gaussian_number2
					# hand_values[i][index_min1] = gaussian_number1
					# hand_values[i][index_min2] = gaussian_number2
				#else:
				# 	print "SUCCESSFUL"
				# print "========================="
			avg = mean(scores)
			avg_scores.append(avg)
			# print "\nAVERAGE SCORE: ", avg
			# print "==============================="
		for hand in population:
			print hand
		for hand_value in hand_values:
			print hand_value
		plot_averages(avg_scores)
		#return [population, hand_values]

def main():
	print "\n\n"
	#print NUM_HANDS

	# population = create_population(n)
	# hand_values = assign_values(n)

	# print "TRAIN PLAYER:  100 hands, 500 times"
	# train_player(100, 500)

	# print "TRAIN PLAYER:  100 hands, 500 times"
	# train_player(100, 500)

	# print "TRAIN PLAYER:  100 hands, 500 times"
	# train_player(100, 500)

	# print "TRAIN PLAYER:  20 hands, 100 times"
	# train_player(20, 100)

	# print "TRAIN PLAYER:  20 hands, 100 times"
	# train_player(20, 100)

	# print "TRAIN PLAYER:  20 hands, 100 times"
	# train_player(20, 100)

	print "TRAIN PLAYER:  1 hands, 5 times"
	train_player(1, 5)

	print "TRAIN PLAYER:  1 hands, 5 times"
	train_player(1, 5)

	print "TRAIN PLAYER:  1 hands, 5 times"
	train_player(1, 5)

	# print "TRAIN PLAYER:  all hands, 50 times"
	# train_player(NUM_HANDS, 50)

	# hand = POSSIBLE_HANDS[10]
	# print "HAND: ", hand
	# pairs = get_pairs(hand)
	# print "PAIRS: ", pairs
	# fifteens = get_fifteens(hand)
	# print "FIFTEENS: ", fifteens
	# runs = get_runs(hand)
	# print "RUNS: ", runs
	# score = get_score(hand)
	# print "\nSCORE: ", score

	# hand_list = [hand]
	# print hand_list
	# value_list = assign_values(2)
	# print value_list
	# write_trained_results('test', hand_list, value_list)

	print "\n"


if __name__ == '__main__':
	main()
