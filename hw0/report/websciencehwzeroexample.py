# must split lyrics into lines, in order to retain the line-level information.
def lyrics_into_lines(lyrics):
    return lyrics.split('\n')

df_balanced['Lyrics_Lines'] = df_balanced['Lyrics'].apply(lyrics_into_lines)

# tokenize each line individually in order to respect the structure of the song.

def tokenize_line(line):
    line = re.sub(r'[^a-zA-Z0-9\s]', '', line.lower())
    tokens = word_tokenize(line)
    return tokens

def tokenize_lyrics(lines):
    return [tokenize_line(line) for line in lines]

df_balanced['Tokenized_Lyrics'] = df_balanced['Lyrics_Lines'].apply(tokenize_lyrics)