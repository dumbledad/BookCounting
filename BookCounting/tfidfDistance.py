# Using Python 3.6

import os, io, math, scipy.spatial
from BookSquishing import squish, squishInDirs

dropBoxRootPath = 'C:\\Users\\timregan\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles3\\'

def totalCount(path, filenames):
    totalCounts = {}

    # Load each book and process it
    for book in filenames:
        with io.open(path + book, "r", encoding="latin-1") as file:
            fileTextRaw = file.read() # Open up the book and read in its entire contents
        words = fileTextRaw.split() # Split into words
        totalCounts[book] = len(words)

    return totalCounts


def wordCount(path, filenames):
    wordCounts = {}

    # Load each book and process it
    for book in filenames:
        print(book)
        with io.open(path + book, "r", encoding="latin-1") as file:
            fileTextRaw = file.read() # Open up the book and read in its entire contents
        words = fileTextRaw.split() # Split into words
        for word in words:
            if word not in wordCounts: 
                # Initialise counts at zero
                wordCounts[word] = {filename: 0 for filename in filenames}
            # Increment count
            wordCounts[word][book] = wordCounts[word][book] + 1

    return wordCounts


def tfidf(wordCounts, totalCounts, filenames):
    # Thanks to https://stevenloria.com/tf-idf/
    tfidfs = {}

    for word in list(wordCounts):
        # Initialise tfidfs at zero
        tfidfs[word] = {filename: 0 for filename in filenames}
        containing = [bk for bk in list(wordCounts[word]) if wordCounts[word][bk] != 0]
        for book in filenames:
            tf = wordCounts[word][book] / totalCounts[book]
            idf = math.log(totalCounts[book] / (1 + len(containing)))
            tfidf = tf * idf
            tfidfs[word][book] = tfidf

    return tfidfs


def similarity(tfidfs, book1, book2):
    # Thanks to https://stats.stackexchange.com/a/47934/9997
    book1Vector = [tfidfs[word][book1] for word in list(tfidfs)]
    book2Vector = [tfidfs[word][book2] for word in list(tfidfs)]
    distance = scipy.spatial.distance.cosine(book1Vector, book2Vector)
    return 1 - distance


# Read the filenames of the books so that we can ingest them
filenames = [fileName for fileName in os.listdir(dropBoxRootPath + 'Texts\\Squished') if fileName.lower().endswith('txt')]

squishInDirs(dropBoxRootPath, False)
totalCounts = totalCount(dropBoxRootPath + 'Texts\\Squished\\', filenames)
wordCounts = wordCount(dropBoxRootPath + 'Texts\\Squished\\', filenames)
tfidfs = tfidf(wordCounts, totalCounts, filenames)
header = ',' + ','.join([ book.replace(',', ' ') for book in filenames ]) + '\n'
csvLines = [header]
for book1 in filenames:
    line = book1 
    for book2 in filenames:
        sim = similarity(tfidfs, book1, book2)
        line = line + ',' + str(sim)
    csvLines.append(line + '\n')
len(csvLines)

# Store the distances in a CSV file
with io.open(dropBoxRootPath + '\\distances.csv', 'w') as outputFile:
    outputFile.writelines(csvLines)


