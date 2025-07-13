import nltk
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

text = "Hello. This is a test."

print(sent_tokenize(text))
