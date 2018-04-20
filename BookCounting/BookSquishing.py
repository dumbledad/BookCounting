import os, io, re
from functools import reduce

path = "E:\\Dropbox\\Projects\\Visualization\\Projectwork\\Miles2\\Texts\\"

# Generic stop words and specific words to ignore. N.B. we cannot include "labour" since we need to keep "new labour"
stopWords = ["a", "about", "after", "all", "also", "an", "and", "any", "around ", "as", "at", "back", "be", "be", "because", "blair", "but", "by", "can", "come", "conservative", "could", "course", "day", "do", "do", "even", "ever", "first", "first", "for", "from", "get", "get", "give", "go", "good", "got", "great", "have", "he", "her", "him", "his", "how", "however", "i", "if", "important", "in", "into", "it", "its", "just", "just", "know", "labour", "like", "look", "major", "make", "make", "may", "me", "means", "measures", "might", "most", "my", "new", "no", "not", "now", "of", "on", "one", "only", "or", "other", "our", "out", "over", "people", "plan", "rather", "regard", "say", "say", "see", "she", "so", "some", "take", "than", "that", "the", "their", "them", "then", "there", "these", "they", "think", "this", "thought", "time", "to", "took", "two", "up", "us", "use", "want", "way", "we", "well", "what", "when", "which", "who", "will", "with", "words", "work", "would", "year", "you", "your"] 
stopPhrases = ["conservative party", "john major", "labour party", "tony blair"]
conflate = [["new labour", "newlabour"]]

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
    elif (str.isspace(char) or char == u"\n") and not str.isspace(string[-1:]): 
        return string + u" " # Keep spaces, but only one and not repeated ones
    else:
        return string # ignore everything else

# Read the sub directories
subDirs = next(os.walk(path))[1]

# Read and process the books in each sub-directory
for subDir in subDirs:
	print(subDir)

	# Read the filenames of the books so that we can ingest them
	bookDir = [fileName for fileName in os.listdir(path + subDir) if fileName.lower().endswith("txt")]

	# If the squish directory does not exist then create it
	if not os.path.exists(path + subDir + "\\Squished"):
		os.makedirs(path + subDir +"\\Squished")

	# Load each book and squish it
	for book in bookDir:
		print(book)
		#Only squish the book if it is not done already
		if not os.path.exists(path + subDir + "\\Squished\\" + book): 
			with open(path + subDir + "\\" + book, "r", encoding="iso8859-1") as file:
				fileTextRaw = file.read() # Open up the book and read in its entire contents
			fileText = str.lower(reduce(squish, fileTextRaw)) # Clean it up using the squish function above
			for conflation in conflate:
				fileText = fileText.replace(conflation[0], conflation[1])
			for stopPhrase in stopPhrases:
				fileText = fileText.replace(stopPhrase, "")
			allWords = fileText.split() # Split into words (or at least runs of characters delimeted by spaces)
			print("length (all words) = ", len(allWords))
			words = [word for word in allWords if not word in stopWords] # Remove the 'stop' words
			print("length (without stop words) = ", len(words))
			words = [word for word in words if len(word.encode("utf-8")) >= 3] # Remove short words that are only one or two characters long #BUG: Why is the 'word' aï making it through?
			print("length (without tiny words) = ", len(words))
			# Store the squished book
			with io.open(path + subDir + "\\Squished\\" + book, "w") as outputFile:
				line = u" ".join(words)
				outputFile.writelines(line)

input("Done. Press 'return' to exit")

