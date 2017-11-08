# Using Python 3.6

import os, io
from functools import reduce

path = "C:\\Users\\timregan\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles2\\Texts\\Squished\\"

# Concepts supplied by Miles, lower-cased and cut to one word only
communityWords = ["community", "opportunity", "responsibility", "society", "rights"]
religionWords = ["religion", "christian", "belief", "conviction"]

# Generic stop words. We could do more to tailor these to our corpus
stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

# Read the filenames of the books so that we can ingest them
bookDir = [fileName for fileName in os.listdir(path) if fileName.lower().endswith("txt")]

# The data structure that will hold the counts of words in each book that are inside or outside each concept
probabilities = {fileName: { 
    "community": { "words": communityWords, "count": [0, 0], "probability": 0 }, 
    "religion": { "words": religionWords, "count": [0, 0], "probability": 0 } } for fileName in bookDir}

# The data structure that will hold the counts of all the words in all the books
wordCounts = {}

# Load each book and process it
for book in bookDir:
    print(book)
    with io.open(path + book, "r", encoding="latin-1") as file:
        fileTextRaw = file.read() # Open up the book and read in its entire contents
    words = fileText.split() # Split into words
    for word in words:
        if not word in wordCounts:
            wordCounts[word] = {}
        if book in wordCounts[word]:
            wordCounts[word][book] += 1 # Increment the word's count from this book in wordcounts
        else:
            wordCounts[word][book] = 1 # Add the word from this book to wordcounts
        for categories, data in probabilities[book].items():
            if word in data["words"]: # data["words"] is the concept list of words
                data["count"] = [ data["count"][0] + 1, data["count"][1] ] # Increment the count of words in the concept
            else:
                data["count"] = [ data["count"][0], data["count"][1] + 1 ] # Increment the count of words outside the concept
    for category, data in probabilities[book].items():
        data["probability"] = float(data["count"][0]) / float(data["count"][0] + data["count"][1]) # Turn the counts into probabilities, i.e. the probability that a word, randomly chosen from this book, will be in this concept
        print(category, data["probability"])

# Store the probabilities in a CSV file
with io.open(path + "probabilities.csv", "w") as outputFile:
    outputLines = [ u",community,religion" ]
    for book in bookDir:
        newOutputLine = book.replace(",", " ") + ","
        newOutputLine = newOutputLine + str(probabilities[book]["community"]["probability"]) + ","
        newOutputLine = newOutputLine + str(probabilities[book]["religion"]["probability"]) 
        outputLines.append(newOutputLine)
    mergedOutputLines = u"\n".join(outputLines)
    outputFile.writelines(mergedOutputLines)

# Store the word counts in a CSV file (in Excel we can add the 'Totals' column and sort rows by that total
with io.open(path + "wordCounts.csv", "w") as outputFile:
    outputLine = u"," + u",".join([ book.replace(",", " ") for book in bookDir ])
    outputLines = [ outputLine ]
    for word in wordCounts:
        newLine = word
        for book in bookDir:
            if book in wordCounts[word]:
                newLine = newLine + u"," + str(wordCounts[word][book])
            else:
                newLine = newLine + u",0" 
        outputLines.append(newLine)
    mergedOutputLines = u"\n".join(outputLines)
    outputFile.writelines(mergedOutputLines)

input("Done. Press 'return' to exit")

