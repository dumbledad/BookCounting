import os, io, csv

path = "C:\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles"

# Load in the Probabilities CSV file saved by the BookCounting.py file
with io.open(path + "probabilities.csv", "r") as file:
    lines = file.readlines()
headers = lines[0].split(",")
probabilities = {} # The data structure to store the probabilities read in from the CSV file
bookNames = [] # List of the book titles for convenience as the keys in a dictionary data structure are not in a gaunteed order
for line in lines[1:]:
    splitLine = line.split(",")
    probabilities[splitLine[0]] = {}
    bookNames.append(splitLine[0])
    for i in range(1, len(headers)):
        key = headers[i]
        value = float(splitLine[i])
        probabilities[splitLine[0]][key] = value

distances = {} # The data structure to hold the results of the distance calculations
for fromBook in probabilities:
    distances[fromBook] = {}
    for toBook in probabilities:
        distance = float(0)
        for concept in headers[1:]:
            distance = distance + (probabilities[toBook][concept] - probabilities[fromBook][concept])**2 # The sum of the squares of the distances
        distance = distance**0.5 # The square root of the sum of the squares of the distances
        distances[fromBook][toBook] = distance

# Store the distances in a CSV file
with io.open(path + "distances.csv", "w") as outputFile:
    outputLine = u"," + u",".join(probabilities)
    outputLines = [ outputLine ]
    for fromBook in bookNames:
        newLine = fromBook
        for toBook in bookNames:
            newLine = newLine + u"," + unicode(distances[fromBook][toBook])
        outputLines.append(newLine)
    mergedOutputLines = u"\n".join(outputLines)
    outputFile.writelines(mergedOutputLines)

raw_input("Done. Press 'return' to exit")
