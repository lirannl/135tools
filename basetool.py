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
    return len(inputSet) == len(set(inputSet))
#Check for bad inputs.
def valuesCheck(inBase, outBase, inputSet, outputSet, charSet, fracPlaces):
    if inBase < 2 or inBase > len(charSet):
        raise ValueError("Input base is out of range")
    if outBase < 0 or outBase > len(charSet):
        raise ValueError("Output base is out of range")
    if inBase > len(inputSet) or outBase > len(outputSet):
        raise ValueError("Custom set doesn't satisfy base")
    if not (isSet(inputSet) or not isSet(outputSet)):
        raise ValueError("Custom set is not unique")
    if search("[.-]", inputSet + outputSet) is not None:
        raise ValueError("Custom set contains - or .")
    if fracPlaces < 0:
        raise ValueError("Negative decimal places invalid")
#Trim inputSet to base.
def trimSet(inputSet, inBase):
    return inputSet[0:inBase] + "."
#Flatten input if possible.
def inputFlatten(inputString, inBase, inputSet, charSet):
    if inBase < 36 and inputSet == charSet: return inputString.lower()
    return inputString
#Check if input is negative.
def inputSign(inString):
    if inString[0] == "-": return inString[1:], True
    return inString, False
#Return list of string indexs.
def inputPosition(absInString, inCutSet):
    inPosList = list(map(lambda char:inCutSet.find(char), absInString))[::-1]
    if -1 in inPosList: raise ValueError("Input characters not in input set")
    return inPosList
#Split decimal inputs.
def inputFloatSplit(inputSet, inPosList):
    if (len(inputSet) - 1) in inPosList: 
        intPosList = inPosList[inPosList.index(len(inputSet)-1) + 1:]
        fracPosList = reversed(inPosList[:inPosList.index(len(inputSet)-1)])
        return intPosList, fracPosList, True
    return inPosList, [], False
#Convert number to Base10.
def convertDecimal(absInString, inBase, inCutSet, inPosList):
    if inCutSet == ["0123456789."]: return str(absInString)
    intPosList, fracPosList, floatInput = inputFloatSplit(inCutSet, inPosList)
    intList = map(lambda pos:(inBase**pos[0])*pos[1], enumerate(intPosList))
    if not floatInput: return sum(intList), False
    fracList = map(lambda pos:(inBase**((pos[0]*-1)-1))*pos[1], enumerate(fracPosList))
    return str(sum(intList) + sum(fracList)), True
#Divmod until quotient is zero.
def inputDivmod(inputQuotient, outBase, remainder = []):
    quotient, remainderList = divmod(inputQuotient, outBase)
    if inputQuotient == 0: return remainder 
    return inputDivmod(quotient, outBase, [int(remainderList)] + remainder)
#Convert number to output base.
def outputPosition(fracInString, outBase, fracPlaces):
    if "." in str(fracInString):
        inputQuotient = float(fracInString) * pow(outBase, fracPlaces)
    else: inputQuotient = int(fracInString)
    return inputDivmod(inputQuotient, outBase)
#Substitute characters to set.
def subCharacters(outPosList, outCutSet):
    return "".join(list(map(lambda pos: outCutSet[pos], outPosList)))
#Format sign and decimal place.
def outputFormat(string, fracPlaces, fracInput, sign):
    if fracInput and fracPlaces != 0: 
        fracString = string[:(fracPlaces*-1)] + "." + string[(fracPlaces*-1):]
    else: fracString = string
    if sign: return "-" + fracString
    return fracString
#Convert base of number.
def baseConvert(inputString:str, inBase:int, outBase:int = 10,
                inputSet:str = charSet, outputSet:str = charSet, fracPlaces:int = 5 ):
    valuesCheck(inBase, outBase, inputSet, outputSet, charSet, fracPlaces)
    inCutSet, outCutSet = trimSet(inputSet, inBase), trimSet(outputSet, outBase)
    inString = inputFlatten(inputString, inBase, inputSet, charSet)
    absInString, sign = inputSign(inString)
    inPosList = inputPosition(absInString, inCutSet)
    fracInString, fracInput = convertDecimal(absInString, inBase, inCutSet, inPosList)
    outPosList = outputPosition(fracInString, outBase, fracPlaces)
    outputString = subCharacters(outPosList, outCutSet)
    return outputFormat(outputString, fracPlaces, fracInput, sign)

print(baseConvert("XXX", 86, 5, outputSet = "Apples"))