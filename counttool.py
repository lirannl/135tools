#Tool to analyse and compare the frequency of each character in a data set.
#Created date: 09/01/2021
category = "tools"
#Format spaces and capitals in input.
def stringFormat(inputString, spaces, capitals):
    if spaces: spaceString = inputString
    else: spaceString = inputString.replace(" ", "")
    if capitals: return spaceString, len(spaceString)
    return spaceString.lower(), len(spaceString)
#Key to order the character dictionary.
def charOrder(inPos):
    _, charCount, charPercent = inPos
    return charCount, charPercent
#Analyse input for character occurrences.
def API_charAnalysis(inputString:str, spaces:bool = True, capitals:bool = True):
    inString, length = stringFormat(inputString, spaces, capitals)
    charSet = list(set(inString))
    countList = list(map(lambda pos:inString.count(pos), charSet))
    percentList = list(map(lambda pos:round((int(pos)/length)*100, 3), countList))
    charDict = zip(charSet, countList, percentList)
    return sorted(charDict, key=charOrder, reverse=True)

