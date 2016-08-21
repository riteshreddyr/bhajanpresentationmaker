__author__ = 'RiteshReddy'
import json
from models.BhajanModel import BhajanModel
def do():
    filename = 'scrapedbhajans.json'
    with open(filename) as input_file:
        d = json.load(input_file)
        for a in d:
            if 'Content' in a.keys():
                bhajan = a['Content'][0]['text']
                bhajan.replace("\n ", "\n")
                title = bhajan.split('\n')[0]
                meaning_and_text = bhajan.split('\n \n')
                text = meaning_and_text[0]
                text_split = text.split('\n')
                for i in range(len(text_split)):
                    text_split[i] = text_split[i].strip()
                text = '\n'.join(text_split)
                meaning = ""
                if len(meaning_and_text) > 1:
                    meaning = meaning_and_text[1]
                    meaning_split = meaning.split('\n')
                    for i in range(len(meaning_split)):
                        meaning_split[i] = meaning_split[i].strip()
                    meaning = '\n'.join(meaning_split)
                BhajanModel.add_bhajan(title, text, meaning)

do()