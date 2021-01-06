#Tool to convert int/float numbers between bases 0-86 with given character sets.
#Created date: 05/01/2021
from math import pow
from re import search
#Default character set.
charSet = "".join([
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '+', '/', '~', '!', '@', '#', '$', '%', '^', '&', 
    '*', ';', '=', '?', '<', '>', '[', ']', ':', '"', '{', '}', ',', '`'])
#Check if inputSet is set.
def isSet(inputSet):
    return len(inputSet) == len(set(inputSet))
#Check for bad inputs.
def valuesCheck(inputBase, outputBase, inputSet, outputSet, charSet, fracPlaces):
    if inputBase < 2 or inputBase > len(charSet):
        raise ValueError("Input base is out of range")
    if outputBase < 0 or outputBase > len(charSet):
        raise ValueError("Output base is out of range")
    if not (isSet(inputSet) or not isSet(outputSet)):
        raise ValueError("Custom set is not unique")
    if search("[.-]", inputSet + outputSet) is not None:
        raise ValueError("Custom set contains - or .")
    if fracPlaces < 0 or fracPlaces > 24:
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
def inputFloatSplit(inputSet, inputPosList):
    if (len(inputSet) - 1) in inputPosList: 
        intPosList = inputPosList[inputPosList.index(len(inputSet)-1) + 1:]
        fracPosList = reversed(inputPosList[:inputPosList.index(len(inputSet)-1)])
        return intPosList, fracPosList, True
    return inputPosList, [], False
#Convert number to Base10.
def convertDecimal(absInString, inputBase, inCutSet, inputPosList):
    if inCutSet == ["0123456789."]: return float(absInString)
    intPosList, fracPosList, floatInput = inputFloatSplit(inCutSet, inputPosList)
    intList = map(lambda pos:(inputBase**pos[0])*pos[1], enumerate(intPosList))
    if not floatInput: return sum(intList)
    fracList = map(lambda pos:(inputBase**((pos[0]*-1)-1))*pos[1], enumerate(fracPosList))
    return (sum(intList) + sum(fracList))
#Convert base of number.
def baseConvert(inputString:str, inputBase:int, outputBase:int = 10,
                inputSet:str = charSet, outputSet:str = charSet, fracPlaces:int = 5 ):
    valuesCheck(inputBase, outputBase, inputSet, outputSet, charSet, fracPlaces)
    inCutSet, outCutSet = trimSet(inputSet, inputBase), trimSet(outputSet, outputBase)
    inString = inputFlatten(inputString, inputBase, inputSet, charSet)
    absInString, sign = inputSign(inString)
    inputPosList = inputPosition(absInString, inCutSet)
    fracInString = convertDecimal(absInString, inputBase, inCutSet, inputPosList)
    return fracInString

print(str(baseConvert("101011.11", 2, 10, fracPlaces = 20)))