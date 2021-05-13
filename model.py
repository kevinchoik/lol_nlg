from collections import defaultdict
import nltk, argparse, random

# List of regions
region_list = ['all', 'bandlecity', 'bilgewater', 'demacia', 'demon', 'ionia',
			   'ixtal','nomad', 'noxus', 'piltover', 'shadowisles', 'shurima',
			   'targon', 'freljord', 'void', 'zaun']

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-r', metavar='REGION', choices=region_list, default='all',
					help='''Region to generate voicelines from:
					all bandlecity bilgewater demacia demon ionia ixtal nomad
					noxus piltover shadowisles shurima targon freljord void zaun''')
parser.add_argument('-g', metavar='NUM_GEN', type=int, default=10, help='Number of lines to generate')
parser.add_argument('-m', metavar='MODEL', type=int, default=1, choices=[0,1,2,3],
					help='''Model to use:
					(0) Simple trigram
					(1) Backoff
					(2) Generation from POS emission''')
args = parser.parse_args()

# Get relevant champions
if args.r == 'all':
	# Grab all champions
	champs_file = open('champs.txt', 'r')
else:
	# Grab only champions from that region
	champs_file = open('./Regions/' + args.r + '.txt', 'r')
champs = champs_file.readlines()
champs = [c.strip() for c in champs]

# Voiceline source
src = './Voicelines/'

# Bigram/trigram probabilities
bigrams = defaultdict(lambda: defaultdict(lambda: 0))
trigrams = defaultdict(lambda: defaultdict(lambda: 0))
# Emission matrix
emission = defaultdict(lambda: defaultdict(lambda: 0))
# Lookup table
lookup = defaultdict(lambda: defaultdict(lambda: 0))

# Set of POSes
posset = set()

# Start and stop symbols
START_SYM = 'START'
STOP_SYM = 'STOP'

# data_size = 0

for c in champs:
	# Retrieve voice lines
	voice_file = open(src + c + '.txt', 'r')
	lines = voice_file.readlines()
	for l in lines:
		tokens = nltk.word_tokenize(l.strip().lower())
		if len(tokens) < 3:
			continue
		# data_size += len(tokens)
		# Previous POS
		pprev_pos = START_SYM
		prev_pos = START_SYM
		# Previous word
		pprev_word = START_SYM
		prev_word = START_SYM
		for word, pos in nltk.pos_tag(tokens):
			# First count the number of occurences
			bigrams[prev_word][word] += 1
			trigrams[(pprev_word, prev_word)][word] += 1
			emission[pos][word] += 1
			# Add to lookup table
			lookup[word][pos] += 1
			# Add to pos set
			posset.add(pos)
			# Advance previous POSes and words
			pprev_pos = prev_pos
			prev_pos = pos
			pprev_word = prev_word
			prev_word = word
		# Add stop token
		bigrams[prev_word][STOP_SYM] += 1
		trigrams[(pprev_word, prev_word)][STOP_SYM] += 1

# Convert counts to probabilities
def count2prob(matrix):
	for entry in matrix.values():
		# Add up counts
		sum = 0
		for count in entry.values():
			sum += count
		# Divide by total count
		for e in entry:
			entry[e] /= sum

count2prob(bigrams)
count2prob(trigrams)
count2prob(emission)

dest_stat = './Stats/'
# Stat 1: Fraction of times 'all' model has only 1 path
# stat_file = open(dest_stat + 'forcedpath.txt', 'w')
# Stat 2: Average fraction of times regional model has only 1 path vs data size
# stat_file = open(dest_stat + 'forcedvssize.txt', 'a')

nopath_list = []
for _ in range(args.g):
	prev = START_SYM
	curr = START_SYM
	words = []
	# Buffer for the model to recover from randomness in model 2
	buffer = 0
	# nopath = 0
	while curr != STOP_SYM:
		# Random value for selection
		rand = random.random()
		# Don't include start symbol
		if curr != START_SYM:
			words.append(curr)
		if args.m != 0 and len(trigrams[(prev, curr)]) <= 1:
			# nopath += 1
			if args.m == 1 or buffer > 0:
				# Model 1: Backoff
				for w, p in bigrams[curr].items():
					rand -= p
					if rand < 0:
						prev = curr
						curr = w
						break
				# Decrement buffer
				if buffer > 0:
					buffer -= 1
			else:
				# Model 2: Convert using emission
				# Grab most probable POS for next word
				next = list(trigrams[(prev, curr)].keys())[0]
				nextpos = None
				maxcount = 0
				for pos, c in lookup[next].items():
					if maxcount < c:
						maxcount = c
						nextpos = pos
				# Go through emission until value hit
				for w, p in emission[nextpos].items():
					rand -= p
					if rand < 0:
						prev = curr
						curr = w
						break
				# Set buffer
				buffer = 2
		else:
			# Model 0: Simple trigram selection
			for w, p in trigrams[(prev, curr)].items():
				rand -= p
				if rand < 0:
					prev = curr
					curr = w
					break
			# Decrement buffer
			if buffer > 0:
				buffer -= 1
	# Output sentence
	print(' '.join(words))

	# stat_file.write(str(nopath / len(words)) + '\n')
	# nopath_list.append(nopath / len(words))

# avg = 0
# for n in nopath_list:
# 	avg += n
# avg /= len(nopath_list)
# stat_file.write(args.r + ' ' + str(avg) + ' ' + str(data_size) + '\n')

# stat_file.close()
