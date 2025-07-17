from nltk import download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

download("stopwords", force=True)
download("punkt_tab", force=True)
words_to_remove = set(stopwords.words("english"))
[words_to_remove.add(word) for word in ['i', 'want', 'eat']]

def generate_title(message):
    words = word_tokenize(message)
    filtered = []
    for word in words:
        if ((word.lower() not in words_to_remove) and (word not in string.punctuation)):
            filtered.append(word)
    
    return ' '.join(filtered[:5]).title() or "Untitled Chat"