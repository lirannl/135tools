#Tool to analyse the frequency of each character in a data set.
#Created date: 09/01/2021
#Key to order the character dictionary.
def charOrder(inPos):
    _, charCount, charPercent = inPos
    return charCount, charPercent
#Analyse input for character occurrences.
def charAnalysis(inputString:str):
    length = len(inputString)
    charSet = list(set(inputString))
    countList = list(map(lambda pos:inputString.count(pos), charSet))
    percentList = list(map(lambda pos:round((int(pos)/length)*100, 3), countList))
    charDict = zip(charSet, countList, percentList)
    return sorted(charDict, key=charOrder, reverse=True)
