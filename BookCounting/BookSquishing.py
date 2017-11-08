import os, io
from functools import reduce

path = "C:\\Users\\timregan\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles2\\Texts\\"

# Generic stop words. We could do more to tailor these to our corpus
stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

# Read the filenames of the books so that we can ingest them
bookDir = [fileName for fileName in os.listdir(path) if fileName.lower().endswith("txt")]

# The function we use to tidy the books into a manageable string
def squish(string, char, keepHyphens = False, keepSentenceEndings = False):
    if char == u"’":
        return string + u"'" # Swap curly apostrophe to straight
    elif keepHyphens and (char == u"-"):
        return string + char # Keep hyphens, dropping by default as often messy in line breaks. Need more work to pull hyphenated words together.
    elif str.isalnum(char) or char == u"–" or char == u"'":
        return string + char # Keep anything alpha-numeric, hyphens, endashes, and apostrophes. We should do more work to only keep these inside a word, not at word boundaries
    elif keepSentenceEndings and ((char == u"." or char == u"!" or char == u"?") and not (string[-1:] == u"." or string[-1:] == u"!" or string[-1:] == u"?")):
        return string + char # Potentially keep sentence endings. Will be useful later if we analyse sentences, but not used for now. In fact we may have to be more sophisticated about parsing sentences if we go down that route
    elif not str.isspace(string[-1:]): 
        return string + " " # Keep spaces, but only one and not repeated ones
    else:
        return string # ignore everything else

# If the squish directory does not exist then create it
if not os.path.exists(path + "Squished"):
    os.makedirs(path + "Squished")

# Load each book and squish it
for book in bookDir:
    print(book)
    #Only squish the book if it is not done already
    if not os.path.exists(path + "Squished\\" + book): 
        with io.open(path + book, "r", encoding="latin-1") as file:
            fileTextRaw = file.read() # Open up the book and read in its entire contents
        fileText = str.lower(reduce(squish, fileTextRaw)) # Clean it up using the squish function above
        allWords = fileText.split() # Split into words (or at least runs of characters delimeted by spaces)
        print("length (all words) = ", len(allWords))
        words = [word for word in allWords if not word in stopWords] # Remove the 'stop' words
        print("length (without stop words) = ", len(words))
        words = [word for word in words if len(word.encode("utf-8")) >= 3] # Remove short words that are only one or two characters long #BUG: Why is the 'word' aï making it through?
        print("length (without tiny words) = ", len(words))
        # Store the squished book
        with io.open(path + "Squished\\" + book, "w") as outputFile:
            line = u" ".join(words)
            outputFile.writelines(line)

input("Done. Press 'return' to exit")

