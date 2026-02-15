import re
from hymnal.models import Hymn

def remove_punctuation(input_string):
    return re.sub(r'[^\w\s]', '', input_string)

def get_hymn_text(title):
    if not title or not title.strip():
        return None  # Handle empty or whitespace-only titles
    
    title = remove_punctuation(title.lower())
    print(f"Searching for hymn: {title}")
    
    # Query database for hymns
    hymns = Hymn.objects.all()
    for hymn in hymns:
        hymn_title_clean = remove_punctuation(hymn.title.lower())
        if title in hymn_title_clean or hymn_title_clean in title:
            print(f"Found hymn: {hymn.title}")
            # Split lyrics into lines and group into stanzas
            lines = [line.strip() for line in hymn.lyrics.split('\n') if line.strip()]
            stanzas = []
            i = 0
            while i < len(lines):
                stanza_lines = []
                while i < len(lines) and len(stanza_lines) < 4:
                    stanza_lines.append(lines[i])
                    i += 1
                if stanza_lines:
                    stanzas.append('\n'.join(stanza_lines))
            return stanzas, hymn.title
    
    print(f"No hymn found for: {title}")
    return None

