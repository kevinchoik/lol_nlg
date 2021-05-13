from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from os import path

# List of champions
champs_file = open('champs.txt', 'r')
champs = champs_file.readlines()
champs = [c.strip() for c in champs]

# Fandom wiki URL
url_prefix = 'https://leagueoflegends.fandom.com/wiki/'
url_suffix = '/LoL/Audio'

# Regular expression to grab voice lines
voiceline = r'"(?<!http)((?:[^"](?!\.ogg))*)"(?:\n| \*)'

# Save destination
dest = './Voicelines/'

for c in champs:
	if (path.isfile(dest + c + '.txt')):
		continue

	# Complete URL
	url = url_prefix + c + url_suffix

	# Extract html
	html = urlopen(url).read()
	soup = BeautifulSoup(html, features='html.parser')
	text = soup.get_text()

	# Find voice lines
	lines = re.findall(voiceline, text)
	lines = [l.strip() + '\n' for l in lines]

	# Save to file
	voice_file = open(dest + c + '.txt', 'w')
	voice_file.writelines(lines)
	voice_file.close()
