########################################################################################
# Tool to analyse and compare the frequency of each character in a data set.
# Creation date: 09/01/2021
########################################################################################
# 135code.com API Category Definition.
category = "tools"

########################################################################################
# Function: stringFormat
# Returns: String with Spaces Optionally Removed and Capitals Optionally Lowered.
def stringFormat(inputString, excludeSpaces, caseSensitive):
    if excludeSpaces: spaceString = inputString.replace(" ", "")
    else: spaceString = inputString
    if caseSensitive: return spaceString, len(spaceString)
    return spaceString.lower(), len(spaceString)

# Function: charOrder
# inPos: Variable that Equals the Desired Order of List Values.
# Returns: Specified List Order.
def charOrder(inPos):
    _, charCount, charPercent = inPos
    return charCount, charPercent

##########################################################################################
# Function: API_charAnalysis
# excludeSpaces: Boolean for if Spaces should be Counted.
# caseSensitive: Boolean for if Capital and Lower Case Characters Should be Seperate.
# Returns: List of Lists Containing Count and Percentage that Character for all Characters.
def API_charAnalysis(inputString:str, 
                     excludeSpaces:bool = True, caseSensitive:bool = True):
    # Format Input with Respect to Case and Spaces Boolean Arguments.
    inString, length = stringFormat(inputString, excludeSpaces, caseSensitive)
    # Create Set of all Unique Characters Contained in Input.
    charSet = list(set(inString))
    # Count the Number of Occurrences of each Character in Character Set.
    countList = list(map(lambda pos:inString.count(pos), charSet))
    # Calculate Percentage of Total Input that is Each Character in Character Set.
    percentList = list(map(lambda pos:round((int(pos)/length)*100, 3), countList))
    # Join Character, Count, and Percentage Lists into one Ordered List of Lists.
    charDict = zip(charSet, countList, percentList)
    return sorted(charDict, key = charOrder, reverse = True)

##########################################################################################