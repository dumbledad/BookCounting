# Using Python 3.6

import os, io, math, scipy.spatial
from BookSquishing import squishInDirs


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


def cosineDistance(tfidfs, book1, book2):
    # Thanks to https://stats.stackexchange.com/a/47934/9997
    book1Vector = [tfidfs[word][book1] for word in list(tfidfs)]
    book2Vector = [tfidfs[word][book2] for word in list(tfidfs)]
    distance = scipy.spatial.distance.cosine(book1Vector, book2Vector)
    return distance


def euclidianDistance(tfidfs, book1, book2):
    book1Vector = [tfidfs[word][book1] for word in list(tfidfs)]
    book2Vector = [tfidfs[word][book2] for word in list(tfidfs)]
    distance = scipy.spatial.distance.euclidean(book1Vector, book2Vector)
    return distance


def csvLine(filenames, tfidfs, distanceFunction):
    header = ',' + ','.join([ book.replace(',', ' ').replace('.txt', '') for book in filenames ]) + '\n'
    csvLines = [header]
    for book1 in filenames:
        line = book1.replace(',', ' ').replace('.txt', '')
        for book2 in filenames:
            dis = distanceFunction(tfidfs, book1, book2)
            line = line + ',' + str(dis)
        csvLines.append(line + '\n')
    return csvLines


def calculateAndWrite(path):
    squishInDirs(path, False)

    filenames = [fileName for fileName in os.listdir(path + 'Texts\\Squished') if fileName.lower().endswith('txt')]

    totalCounts = totalCount(path + 'Texts\\Squished\\', filenames)
    wordCounts = wordCount(path + 'Texts\\Squished\\', filenames)
    tfidfs = tfidf(wordCounts, totalCounts, filenames)
    cosineCsvLines = csvLine(filenames, tfidfs, cosineDistance)
    euclideanCsvLines = csvLine(filenames, tfidfs, euclidianDistance)

    # Store the distances in a CSV file
    with io.open(path + '\\cosineDistances.csv', 'w') as outputFile:
        outputFile.writelines(cosineCsvLines)
    with io.open(path + '\\euclideanDistances.csv', 'w') as outputFile:
        outputFile.writelines(euclideanCsvLines)


