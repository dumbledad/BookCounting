#Use Python 2.7

import os, io, re, ntlk

path = "C:\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles\\"

# Concepts supplied by Miles, lower-cased and cut to one wor only
islamWords = ["total", "complete", "religious", "jihad", "conscience", "submission", "zedegi", "fundamentalist", "modernist", "secular", "fanon", "hadith", "allah", "god"]
colonialismWords = ["westoxification", "west", "imperial", "colonial", "alienation", "isolation", "apart", "alone", "imperialism", "colonialism", "algeria"]
marxismWords = ["revolution", "violence", "class", "economic", "production", "stage", " marxism", "moral", "decay", "morality"]
nationalismWords = ["iran", "iraq", "arab", "west", "nation", "sovereign", "law", "ayotollah", "leader", "algeria", "constitution"]
capitalismWords = ["money", "greed", "avarice", "corruption", "corporation", "oil", "nationalization", "weakness"]
violenceWords = ["struggle", "fight", "gun", "shoot", "guns", "overthrow", "kill", "injure", "harm"]

# Generic stop words. We could do more to tailor these to our corpus
stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

# Read the filenames of the books so that we can ingest them
bookDir = [fileName for fileName in os.listdir(path) if fileName.lower().endswith("txt")]

multipleSpacesRegex = re.compile(ur"\s\s+")
wordsRegex = re.compile(ur"(?u)\w+")
sentencesRegex = re.compile(ur"[^\.\,\?\!](.*)[\.\,\?\!]")

probabilities = {}

# Load each book and process it
for book in bookDir:
    print book
    with io.open(path + book, "r", encoding="latin-1") as file:
        fileTextRaw = file.read() # Open up the book and read in its entire contents
        fileTextSingleSpaces = re.sub(multipleSpacesRegex, " ", fileTextRaw) 
        words = re.findall(wordsRegex, fileTextSingleSpaces)
        sentences = re.findall(sentencesRegex, fileTextSingleSpaces)
    break


