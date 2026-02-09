import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from unidecode import unidecode

def remove_punctuation(input_string):
    return re.sub(r'[^\w\s]', '', input_string)

def find_best_tag(result_tags, inp_lower):
    # First try exact match
    for tag in result_tags:
        tag_text = remove_punctuation(unidecode(tag.get_text().lower()))
        if inp_lower == tag_text:
            return tag
    
    # If no exact match, try partial match (title contained in link text)
    for tag in result_tags:
        tag_text = remove_punctuation(unidecode(tag.get_text().lower()))
        if inp_lower in tag_text:
            return tag
    
    return None

def get_hymn_text(title):
    if not title or not title.strip():
        return None  # Handle empty or whitespace-only titles
    
    title = remove_punctuation(title.lower())
    try:
        with requests.Session() as session:
            response = session.get(f'http://www.hymntime.com/tch/ttl/ttl-{title[0]}.htm')
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('a')
            link = find_best_tag(results, title)
            if link is None:
                return None  # Hymn not found
            response = session.get(f'http://www.hymntime.com/tch/ttl/{link["href"]}')
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics_div = soup.find(class_='lyrics-text')
            if not lyrics_div:
                return None
            # Get all text and replace br with newlines
            for br in lyrics_div.find_all('br'):
                br.replace_with('\n')
            full_text = lyrics_div.get_text()
            # Normalize line endings
            full_text = full_text.replace('\r\n', '\n').replace('\r', '\n')
            # Split by newlines to get individual lines
            verses = [verse.strip() for verse in full_text.split('\n') if verse.strip()]
            # Group lines into stanzas of 4
            hymn_text = []
            i = 0
            while i < len(verses):
                stanza_lines = []
                while i < len(verses) and len(stanza_lines) < 4:
                    stanza_lines.append(verses[i])
                    i += 1
                stanza = '\n'.join(stanza_lines)
                hymn_text.append(stanza)
            return hymn_text, title
    except RequestException:
        return None

