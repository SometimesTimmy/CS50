import cs50
import sys
import os
import nltk
# natural language toolkit
# note that nltk has a method called tokenize(s) which can split a str object (e.g. a 140 character tweet) into a list of words (shorter str objects)

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        # don't include the comments. Use str.strip and str.startswith(;) to strip away lines that starts with ";"

        self.positives_set = set()
        self.negatives_set = set()

        file = open(positives, "r")
        for line in file:
            if not line.startswith(';'):
                self.positives_set.add(line.rstrip("\n"))
        file.close()

        file = open(negatives, "r")
        for line in file:
            if not line.startswith(';'):
                self.negatives_set.add(line.rstrip("\n"))
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        # take the tweet break it apart into individual words using tokenize

        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)

        score = 0
        positives = 0
        negatives = 0
        for word in tokens:
            if word.lower() in self.positives_set:
                positives += 1
            elif word.lower() in self.negatives_set:
                negatives += 1

        neutral = len(tokens) - positives - negatives
        score = positives - negatives
        return score
