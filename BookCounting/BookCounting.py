# Using Python 3.6

import os, io
from functools import reduce

path = "C:\\Users\\timregan\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles2\\Texts\\"

# Concepts supplied by Miles, lower-cased and cut to one word only
communityWords = ["community", "communities", "society", "civil society", "civil", "people", "cohesion", "individual", "alone", "stakeholder", "stake", "decency", "mutual", "local", "regional", "neighbourhood", "relation", "relationship", "relationships", "active", "activism", "collective", "behaviour", "group", "social", "culture", "allegiance", "trust", "charity", "autonomy", "compassion", "owe", "partner", "diversity", "liberty", "communication", "emancipate", "social"] 
religionWords = ["christian", "protestant", "catholic", "justice", "secular", "atheist", "belief", "tolerance", "experiences", "moral", "ethical", "compassion", "faith", "christian", "congregation", "church", "religious", "religion", "gospels", "christ", "god"]
socialWords = ["social", "socialism", "mutual", "public", "personal", "self-interest", "group", "community", "interdependence", "cooperative", "reciprocal", "needs"]
familyWords = ["family", "local", "children", "lives", "shelter", "parent", "parents", "home", "homes", "wife", "husband", "sex", "families"]
economicsWords = ["work", "economic", "market", "economics", "invest", "competition", "stability", "growth", "nationalisation", "ownership", "compete", "neoliberal", "profit", "risk", "productive", "efficiency", "inequality", "enterprise", "regulation", "dynamic", "tech", "prudence", "prosperity", "tax", "consumers"]
educationWords = ["school", "schools", "maths", "nurseries", "university", "local authorities", "young", "education", "young people", "skills", "literacy", "educational"] 
healthWords = ["poverty", "nhs", "n.h.s.", "health", "waiting list", "hospital", "care", "clinical", "patient"] 
crimeWords = ["behaviour", "culture", "security", "discipline", "fear", "poverty", "urban", "offenders", "violent crime", "crime", "police", "prosecute", "drugs", "victims"]
environmentWords = ["environment", "pollution", "sustainable", "sustainability", "climate change", "countryside", "forests", "carbon", "clean", "rural"]
welfareWords = ["welfare", "compassion", "culture", "depend", "dependence", "benefits", "insecure", "survival", "social security", "unemployment"] 
europeWords = ["europe", "eu", "union", "brussels"]
foreignPolicyWords = ["global", "nation", "security", "international", "peace", "war"]
constitutionWords = ["authority", "rule", "constitution", "devolution", "House of Lords", "government"]
thirdWayWords = ["third way", "values", "duties", "rights", "stake", "stakeholder", "stakeholders", "responsibility", "responsibilities", "change", "reform", "middle", "third way", "justice", "idea", "ideology", "opportunity", "equal", "obligation", "obligations", "freedom", "stability", "ethic", "commit", "history", "identity", "culture", "trust", "progressive", "enterprise", "philosophy", "modern", "choice", "fair", "reciprocal", "entrepreneur", "devolution", "open", "accountability", "consensus", "redistribution"]

# Generic and project specific stop words
stopWords = ["a", "about", "after", "all", "also", "an", "and", "any", "around ", "as", "at", "back", "be", "be", "because", "blair", "but", "by", "can", "come", "conservative", "could", "course", "day", "do", "do", "even", "ever", "first", "first", "for", "from", "get", "get", "give", "go", "good", "got", "great", "have", "he", "her", "him", "his", "how", "however", "i", "if", "important", "in", "into", "it", "its", "just", "just", "know", "labour", "like", "look", "major", "make", "make", "may", "me", "means", "measures", "might", "most", "my", "new", "no", "not", "now", "of", "on", "one", "only", "or", "other", "our", "out", "over", "people", "plan", "rather", "regard", "say", "say", "see", "she", "so", "some", "take", "than", "that", "the", "their", "them", "then", "there", "these", "they", "think", "this", "thought", "time", "to", "took", "two", "up", "us", "use", "want", "way", "we", "well", "what", "when", "which", "who", "will", "with", "words", "work", "would", "year", "you", "your"] 

# Read the sub directories
subDirs = next(os.walk(path))[1]

# Read and process the books in each sub-directory
for subDir in subDirs:
    print(subDir + "\\Squished")

    # Read the filenames of the books so that we can ingest them
    bookDir = [fileName for fileName in os.listdir(path + subDir + "\\Squished") if fileName.lower().endswith("txt")]

    # The data structure that will hold the counts of words in each book that are inside or outside each concept
    probabilities = {fileName: { 
        "community": { "words": communityWords, "count": [0, 0], "probability": 0 }, 
        "religion": { "words": religionWords, "count": [0, 0], "probability": 0 }, 
        "social": { "words": socialWords, "count": [0, 0], "probability": 0 }, 
        "family": { "words": familyWords, "count": [0, 0], "probability": 0 }, 
        "economics": { "words": economicsWords, "count": [0, 0], "probability": 0 }, 
        "education": { "words": educationWords, "count": [0, 0], "probability": 0 }, 
        "health": { "words": healthWords, "count": [0, 0], "probability": 0 }, 
        "crime": { "words": crimeWords, "count": [0, 0], "probability": 0 }, 
        "environment": { "words": environmentWords, "count": [0, 0], "probability": 0 }, 
        "welfare": { "words": welfareWords, "count": [0, 0], "probability": 0 }, 
        "europe": { "words": europeWords, "count": [0, 0], "probability": 0 }, 
        "foreignPolicy": { "words": foreignPolicyWords, "count": [0, 0], "probability": 0 }, 
        "constitution": { "words": constitutionWords, "count": [0, 0], "probability": 0 }, 
        "thirdWay": { "words": thirdWayWords, "count": [0, 0], "probability": 0 } } for fileName in bookDir}

    # The data structure that will hold the counts of all the words in all the books
    wordCounts = {}

    # Load each book and process it
    for book in bookDir:
        print(book)
        with io.open(path + subDir + "\\Squished\\" + book, "r", encoding="latin-1") as file:
            fileTextRaw = file.read() # Open up the book and read in its entire contents
        words = fileTextRaw.split() # Split into words
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
            data["probability"] = 0
            if float(data["count"][0]) != 0:
                data["probability"] = float(data["count"][0]) / float(data["count"][0] + data["count"][1]) # Turn the counts into probabilities, i.e. the probability that a word, randomly chosen from this book, will be in this concept
            print(category, data["probability"])

    # Store the probabilities in a CSV file
    with io.open(path + subDir + "\\probabilities.csv", "w") as outputFile:
        outputLines = [ u",community,religion,social,family,economics,education,health,crime,environment,welfare,europe,foreign policy,constitution,third way" ]
        for book in bookDir:
            newOutputLine = book.replace(",", " ") + ","
            newOutputLine = newOutputLine + str(probabilities[book]["community"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["religion"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["social"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["family"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["economics"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["education"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["health"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["crime"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["environment"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["welfare"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["europe"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["foreignPolicy"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["constitution"]["probability"]) + ","
            newOutputLine = newOutputLine + str(probabilities[book]["thirdWay"]["probability"]) 
            outputLines.append(newOutputLine)
        mergedOutputLines = u"\n".join(outputLines)
        outputFile.writelines(mergedOutputLines)

    # Store the word counts in a CSV file (in Excel we can add the 'Totals' column and sort rows by that total
    with io.open(path + subDir + "\\wordCounts.csv", "w") as outputFile:
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
