import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.data import find

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def split_sentences(text):
    # Load tokenizer manually from 'punkt' folder
    tokenizer_path = find('tokenizers/punkt/english.pickle')
    with open(tokenizer_path, 'rb') as f:
        tokenizer = PunktSentenceTokenizer.load(f)
    return tokenizer.tokenize(text)
