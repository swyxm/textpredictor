# Name:         Swayam Parekh
# Date:         May. 20, 2022
# Class:        ICS3U1-04
# Description:  This text predictor along with a "machine learning" feature, lets you type entire paragraphs and at any given moment when the user hits enter, based on the user's previously entered words, the program will display the top three text predictions. The user can select and continue typing out their sentence until they hit enter twice for the final sentence to be printed out. Based on the user's typing habits, the text predictor adapts and expands and learns which words are typed more, to be stored back into the file for later use.

#For Mac, the file will only open if I write out the path to the file that's on my computer. It may show an error on a different computer but it just needs to be replaced.
dictFile = open("/Users/swayam/Downloads/dict.txt", "r")

#Setting up blanklists to store the words from the textfile in various formats for various purposes.
fileWords = []
wordbank=[]
occurences=[]
sortedWords = []
sortedOccurences = []
newWords = []
#Used to store punctuation that the program does not wish to store in the text preciction database.
unwantedPunctuation = [".","?",",",":",";","[","]","/",">","<","(",")","*","^","%","$","#","!","`","~","|","{","}"]

#Loop is used to sift through the entire file and append all unique words.
while True:
	#Reading the textfile and removing the new line.
	text = dictFile.readline()
	text = text.rstrip("\n")

	#Ensuring duplicate words are not appended to the list but the occurences counter is updated in the related index.
	if text in wordbank:  
		textPos = wordbank.index(text)
		occurences[textPos]+=1
	#This is put before so that a blank string doesn't show up at the end of the wordbank.
	elif text=="": 
		break 
	#Appends unique words.
	else:
		wordbank.append(text)
		occurences.append(1)  
dictFile.close()

#The file needs to be closed and reopened when the contents are being added to another list so that the readline() command restarts and the list isn't blank.
dictFile = open("/Users/swayam/Downloads/dict.txt", "r")
while True:
	#variables need to be redefined once more
	text = dictFile.readline()
	text = text.rstrip("\n")    
	if text == "":
		break
	else:
		#This portion is key for the "machine learning" feature. The wordbank list stores unique words which means the number of times a word appears is lost. Filewords stores all the words in its raw form so the feature works accurately.
		fileWords.append(text)

#Initializes the accumulator variable
occurenceSorter = 1 
#This portion of the program seems to only work with a while loop which helps ensure the sorted list is equivalent to the wordbank list so the for loop doesn't mess up the sorting.
while True:
	#The for loop ensures that each word stored in the wordbank list ends up being sorted.
	for words in wordbank:
		#Appends all the least occuring words and then the accumulator increases by one and checks for the next least occuring words.
		if occurenceSorter == occurences[wordbank.index(words)]:
			sortedWords.append(words)
			sortedOccurences.append(occurences[wordbank.index(words)])
	occurenceSorter+=1 

	#Breaks the loop and reverses the sorted lists, once both lists have been sorted by checking if the same amount of words have been included as in the unsorted lists.
	if len(sortedWords) == len(wordbank):
		sortedWords.reverse()
		sortedOccurences.reverse()
		break

#Sets up the input area for the user. newSentence is a blank input so that the sentence continuation feature works. The normal input prompt, that's supposed to be there, is the print statement above it.
print("Enter text below: ")
newSentence = ""

#The main loop is so that the program will continue to repeat unless the user wishes to exit.
while True: 
	#The sentence variable is seperate so that newSentence always stores the latest entry by the user, while the rest is saved in the sentence variable.
	sentence = input(newSentence)
	#Checks if the user hit the enter key to finalize their sentence. The final word will then be printed, ready to be copied and pasted.
	if sentence.lower() == "":
		print ("\nFinal Sentence: \n" + newSentence.capitalize())
		break
	else:
		#Creates a new variable to store the last word in a user's sentence, to be checked for text prediction, so that the string in the sentence variable is not modified and still stores the user's previous entry. An index variable is also created.
		wordInput = sentence
		index = 0

		#The for loop is used to find each space in a string using the variable "spaces"
		for spaces in wordInput:
			spaces = wordInput.find(" ")

			#The for loop will break before spaces is stored as -1 so that the last word the user typed is printed out properly with the correct index. (The correct index is the one before -1)
			if spaces == -1:
				break
			#This portion is what slices every part before a space, until it reaches the last space. It is put after the if statement so spaces isn't -1.
			else:
				#1 is added because indexing starts at 0 and messes up the position where the string must be sliced, affecting wordInput for its later use.
				wordInput = sentence[spaces+1:]     
				index += spaces+1
				wordInput = sentence[index:] 

		#Sets up a counter variable.
		count = 0
		#Sets up the choices list (initialized within the loop so it goes blank each time, for a new word)
		choices = []  
		#The for loop is used so that each word that meets the prediction criteria is counted by the program.
		for words in sortedWords:
			#Finds words that start with the same sequence of letters as the portion of text the user wants to be predicted.
			if wordInput == words[:len(wordInput)]: 
				#counter variable goes up by 1 for each word it finds sequentially. Because the list is sorted, the top three words will only be appended and printed in order.
				if count<3:
					count +=1
					print("Word #"+str(count)+":", words,sortedOccurences[sortedWords.index(words)])
					choices.append(words)

		#The while loop ensures there is proper error handling if the user accidentally enters a number outside the list range.
		while True: 
			#Checks if there are any words appended to the choice list. If not, the sentence will be repeated back and the user can continue typing more or hit enter to end.
			if choices == []:
				print("There are no matching words in the database")
				newSentence = newSentence + (sentence)
				break
			else:
				#Prompts the user to select a word from the options
				wordSelection = input("Pick the word based on its corresponding number: ")
				#If the user decides in the middle not  to use the text predicting feature but wished to finish the sentence before exitimg, this acts as an error handler.
				if wordSelection.lower() == "": 
					print("\nFinal Sentence: \n" + newSentence.capitalize() + sentence)
					break    
				#Checks if the selection is within the range of choices. If not, the loop will repeat. Based on the selection, newSentence is modified and replaced with the selected word. The index variable from before is used to place it in the proper spot.
				elif int(wordSelection)<=len(choices):   
					newSentence = newSentence + (sentence[:index]+choices[int(wordSelection)-1])
					break

#The for loop is so that all unwanted punctuation attached to a word is removed from the newSentence variable.
for punctuation in unwantedPunctuation:
	if punctuation in newSentence:
		newSentence = newSentence.replace(punctuation,"")
#newWords is the list that stores individual words from newSentence.
newWords = newSentence.split()

#The loop ensures fileWords, the master list that includes duplicates has the new words appended. This is the "machine learning" element.
for newWord in newWords:
	fileWords.append(newWord)
#The file is closed because the reading of the file is over. The new words must be written into the file.
dictFile.close()

#The file is reopened.
dictFile = open("/Users/swayam/Downloads/dict.txt", "w")
#The for loop is so that every word, along with the new onces, as well as the duplicate occurences, is included in the dict file.
for allWords in fileWords:
	dictFile.write(allWords + "\n")
dictFile.close()

