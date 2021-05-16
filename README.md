# lol_nlg
Natural Language Generation of League of Legends Voice Lines

Final Project for LING 227

Dependencies: Beautiful Soup (bs4)

## Scraping

To scrape all voice lines from League of Legends FANDOM wiki, run: ```python3 scrape.py```

## Post-processing

To post-process the voice lines, run: ```python3 process.py```

All voice lines after post-processing and additional manual processing is in the Voicelines/ folder.

## Running the model

To run the model, run: ```python3 model.py```

There are several parameters:
* ```-r REGION```: Region to generate the voice lines from (default = all)
  * List of regions:
    * all
    * bandlecity
    * bilgewater
    * demacia
    * demon
    * ionia
    * ixtal
    * nomad
    * noxus
    * piltover
    * shadowisles
    * shurima
    * targon
    * freljord
    * void
    * zaun
* ```-g NUM_GEN```: Number of lines to generate (default = 10)
* ```-m MODEL```: Model to use (default = 1)
  * 0: Simple trigram
  * 1: Backoff
  * 2: Generation from POS emission
