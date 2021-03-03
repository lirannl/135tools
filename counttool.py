########################################################################################
#Tool to analyse and compare the frequency of each character in a data set.
#Created date: 09/01/2021

########################################################################################
#135code.com API Category Definition.
category = "tools"

#Format spaces and capitals in input.
def stringFormat(inputString, excludeSpaces, caseSensitive):
    if excludeSpaces: spaceString = inputString.replace(" ", "")
    else: spaceString = inputString
    if caseSensitive: return spaceString, len(spaceString)
    return spaceString.lower(), len(spaceString)
    
#Key to order the character dictionary.
def charOrder(inPos):
    _, charCount, charPercent = inPos
    return charCount, charPercent

#Analyse input for character occurrences.
def API_charAnalysis(inputString:str, excludeSpaces:bool = True, caseSensitive:bool = True):
    inString, length = stringFormat(inputString, excludeSpaces, caseSensitive)
    charSet = list(set(inString))
    countList = list(map(lambda pos:inString.count(pos), charSet))
    percentList = list(map(lambda pos:round((int(pos)/length)*100, 3), countList))
    charDict = zip(charSet, countList, percentList)
    return sorted(charDict, key=charOrder, reverse=True)

########################################################################################