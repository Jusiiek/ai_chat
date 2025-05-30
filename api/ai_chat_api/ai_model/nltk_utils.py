import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

nltk.download('punkt_tab')

steamer = PorterStemmer()

def tokenize(sentence):
  return nltk.word_tokenize(sentence)

def stem(word):
  """
  returns the stemmed version of a word
  """
  return steamer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
  """
  returns a bag of words array

  sentence = ["hello", "how", "are", "you"]
  words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
  bag = [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0]
  """
  tokenized_sentence = [stem(w) for w in tokenized_sentence]
  bag = np.zeros(len(all_words), dtype=np.float32)
  for idx, w in enumerate(all_words):
    if w in tokenized_sentence:
      bag[idx] = 1.0
  return bag