import re

# List of champions
champs_file = open('champs.txt', 'r')
champs = champs_file.readlines()
champs = [c.strip() for c in champs]

for c in champs:
	# Grab file contents
	voice_file = open('./Voicelines/' + c + '.txt', 'r')
	lines = voice_file.readlines()

	newlines = []
	for l in lines:
		# Remove expressions
		newl = re.sub(r'\*[^\*]*\*', '', l)
		newl = re.sub(r'\([^\)]*\)', '', newl)
		# Fix ellipses
		newl = re.sub(r'(?<!\.)\.\.(?!\.)', '...', newl)
		newl = re.sub(r'\.{4,}', '...', newl)
		newl = re.sub('…', '...', newl)
		newlines.append(newl)

	# Close and reopen for write	
	voice_file.close()
	voice_file = open('./Voicelines/' + c + '.txt', 'w')
	voice_file.writelines(newlines)
	voice_file.close()
