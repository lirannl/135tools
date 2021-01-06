#Tool to convert int/float numbers between bases 0-86 with given character sets.
#Created date: 05/01/2021
from math import pow
from re import search
#Default character set.
charSet = "".join([
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
    'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '+', '/', '~', '!', '@', '#', 
    '$', '%', '^', '&', '*', ';', '=', '?', '<', '>', '[', ']', ':', '"', '{', '}', ',', 
    '`'])
#Check if inputSet is set.
def isSet(inputSet):
    if len(inputSet) == len(set(inputSet)): return True
    return False
#Check for bad inputs.
def valuesCheck(inputBase, outputBase, inputSet, outputSet, charSet, decimals):
    if inputBase < 0 or inputBase > len(charSet):
        raise ValueError("Input base is out of range")
    if outputBase < 0 or outputBase > len(charSet):
        raise ValueError("Output base is out of range")
    if (isSet(inputSet) or isSet(outputSet)) is False:
        raise ValueError("Custom set is not unique")
    if search("[.-]", inputSet + outputSet) is not None:
        raise ValueError("Custom set contains - or .")
    if decimals < 0 or decimals > 24:
        raise ValueError("Number decimals is out of range")
#Trim inputSet to base.
def trimSet(inputSet, inputBase):
    return inputSet[0:inputBase] + "."
#Flatten input if possible.
def inputFlatten(inputString, inputBase, inputSet, charSet):
    if inputBase < 36 and inputSet == charSet: return inputString.lower()
    return inputString
#Check if input is negative.
def inputSign(inString):
    if inString[0] == "-": return inString[1:], True
    return inString, False
#Return list of string indexs.
def inputPosition(absInString, inCutSet):
    inputPosList = list(map(lambda char:inCutSet.find(char), absInString))[::-1]
    if -1 in inputPosList: raise ValueError("Input characters not in input set")
    return inputPosList
#Split decimal inputs.
def inputDecSplit(inputSet, inputPosList):
    if (len(inputSet) - 1) in inputPosList: 
        intPosList = inputPosList[inputPosList.index(len(inputSet)-1) + 1:]
        decPosList = reversed(inputPosList[:inputPosList.index(len(inputSet)-1)])
        return intPosList, decPosList, True
    intPosList = inputPosList
    return intPosList, [], False
#Convert number to Base10.
def convertDecimal(absInString, inputBase, inCutSet, inputPosList):
    if inCutSet == ["0123456789."]: return absInString
    intPosList, decPosList, floatInput = inputDecSplit(inCutSet, inputPosList)
    intList = map(lambda pos:(inputBase ** pos[0])*pos[1], enumerate(intPosList))
    if not floatInput: return sum(intList)
    decList = map(lambda pos:(inputBase ** (pos[0]*-1)-1)*pos[1], enumerate(decPosList))
    print(list(decList))
    return (sum(intList) + sum(decList))
#Convert base of number.
def baseConvert(inputString:str, inputBase:int, outputBase:int = 10,
                inputSet:str = charSet, outputSet:str = charSet, decimals:int = 5 ):
    valuesCheck(inputBase, outputBase, inputSet, outputSet, charSet, decimals)
    inCutSet, outCutSet = trimSet(inputSet, inputBase), trimSet(outputSet, outputBase)
    inString = inputFlatten(inputString, inputBase, inputSet, charSet)
    absInString, sign = inputSign(inString)
    inputPosList = inputPosition(absInString, inCutSet)
    if outputBase == 0: return 42
    decInString = convertDecimal(absInString, inputBase, inCutSet, inputPosList)
    return decInString

print(str(baseConvert("101011.11", 2, 10, decimals = 20)))
