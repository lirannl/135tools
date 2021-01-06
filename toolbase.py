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

#Check if input is set.
def checkSet(input):
    if len(input) == len(set(input)): return False
    return True

#Check for input errors.
def errorCheck(inputBase, outputBase, inputSetFull, outputSetFull, charSet, places):
    if (inputBase or outputBase) < 0:
        raise ValueError("Zero or Negative Base Values")
    if (inputBase or outputBase) > len(charSet):
        raise ValueError("Base values exceed symbol limit")
    if (checkSet(inputSetFull) or checkSet(outputSetFull)) is True:
        raise ValueError("Input or Output set is not unique")
    if places < 0 or places > 24:
        raise ValueError("Decimal places input is invalid")
    if search("[.-]", (inputSetFull + outputSetFull)) is not None: 
        raise ValueError("Custom character set contains - or .") 

#Correct for input errors.
def inputCorrection(input, inputBase, inputSetFull,):
    if inputBase < 36 and inputSetFull == charSet: return input.lower()
    return input

#Check if input is + or -.
def signCheck(input):
    if input[0] == "-": return (True, input[1:])
    return (False, input)

#Substitute function.
def substituteChar(outputSet, posList, negative, places = 0, input = ""):
    if places != 0 and "." in input:
        absPosList = (list(map(int, posList)))
        floatInput = True 
    else: absPosList, floatInput = posList, False
    subList = list(map(lambda point: outputSet[point], absPosList))
    if floatInput: subList.insert(places * -1, ".")
    if negative: return "-" + "".join(subList)
    return "".join(subList)

#Same base, substitute symbols.
def substituteInput(inputSet, outputSet, negative, positiveInput, inputPosList):
    if inputSet == outputSet:
        if negative: return "-" + positiveInput
        return positiveInput
    return substituteChar(outputSet, inputPosList, negative)

#Convert to Base10 if needed.
def decimalConvert(inputSet, inputBase, charSet, positiveInput, inputPosList):
    if inputSet == charSet[:9] + "-": return positiveInput
    if (len(inputSet) - 1) in inputPosList: 
        intPosList = inputPosList[inputPosList.index(len(inputSet)-1) + 1:]
        decPosList = reversed(inputPosList[:inputPosList.index(len(inputSet)-1)])
        floatInput = True
    else: intPosList, floatInput = inputPosList, False
    decimalList = map(lambda point: 
                  (inputBase ** point[0]) * point[1], enumerate(intPosList))
    if not floatInput: return sum(decimalList)
    floatList = map(lambda point:
                (inputBase ** (point[1] * -1)) * point[1], enumerate(decPosList))
    return (sum(decimalList) + sum(floatList))

#Convert to decimal base.
def inputBaseConvert(correctInput, inputSet, outputSet):
    if len(inputSet) == len(outputSet):
        result = list(map(lambda char:inputSet.find(char), correctInput))
    else: result = list(map(lambda char:inputSet.find(char), correctInput))[::-1]
    if -1 in result:
        raise ValueError("Input characters not present in input set")
    return result

#Convert to output base.
def outputBaseConvert(outputBase, quotient, places, remainder = []):
    if remainder == [] and isinstance(quotient, float):
        inputQuotient = quotient * pow(outputBase, places)
    else: inputQuotient = quotient
    if inputQuotient == 0: return remainder
    newQuotient, newRemainder = divmod(inputQuotient, outputBase)
    return outputBaseConvert(outputBase, newQuotient, places, 
                             [newRemainder] + remainder)

#Convert number base with error checking.
def baseConvert(inputString:str, inputBase:int, outputBase:int = 10, 
                inputSetFull:str = charSet, outputSetFull:str = charSet, 
                places:int = 5):
    if outputBase == 0: return 42 
    (negative, positiveInput) = signCheck(inputString)
    errorCheck(inputBase, outputBase, inputSetFull, 
               outputSetFull, charSet, places)
    correctInput = inputCorrection(positiveInput, inputBase, inputSetFull)
    inputSet = inputSetFull[0:inputBase] + "."
    outputSet = outputSetFull[0:outputBase] + "."
    inputPositionList = inputBaseConvert(correctInput, inputSet, outputSet)
    if inputBase == outputBase:
        return substituteInput(inputSet, outputSet, negative, 
                               correctInput, inputPositionList)
    print(inputPositionList)
    decimalInput = decimalConvert(inputSet, inputBase, charSet, 
                                  correctInput, inputPositionList)
    outputPositionList = outputBaseConvert(outputBase, decimalInput, places)
    return substituteChar(outputSet, outputPositionList, negative, places, inputString)
#101110101.1
#1KxsB.4elwg0000000000
print(baseConvert("101011.11", 2, 10, places = 20))