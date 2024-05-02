import requests
from lxml.html import fromstring
import json
import string
from collections import Counter


"""
    Initiates scraping of Microsoft's Wikipedia Page
"""
def start():

    number = input("""
     __                __                __                   
    /   _ _    | _ _  /   _  _|. _  _   /  |_  _ || _ _  _  _ 
    \__| (_|\)/|(-|   \__(_)(_||| )(_)  \__| )(_|||(-| )(_)(- 
                                   _/                   _/    
    - Aaron McCarthy
    - https://github.com/amccarthy9904/microsoft_web_scraper                                                            
                                                            
    Enter number of words to return (default = 10)\n""")
    number = int(number) if number else 10
    to_exclude = input('Enter words to exclude seperated by a space\n')
    to_exclude = set(to_exclude.split(' '))
    to_exclude.update(['', ' ', '–'])

    resp = requests.get('https://en.wikipedia.org/wiki/Microsoft')
    page = fromstring(resp.text)

    curr = page.xpath('//h2/span[@id="History"]/..')[0]
    text = ''
    curr = curr.getnext().getnext()
    while curr is not None and curr.tag != 'h2':
        text += curr.text_content() + ' '
        curr = curr.getnext()

    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    text = text.translate(str.maketrans(' ', ' ', string.digits))
    text = text.split(' ')
    
    c = Counter()
    l = 0
    for word in text:
        clean_word = word.lstrip().rstrip().lower()
        if clean_word not in to_exclude:
            l = max(l, len(clean_word))
            c[clean_word] += 1
    
    for pair in c.most_common(number):
        print('| {:14} | {:3} |'.format(*pair))

start()