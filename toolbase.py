#Tool to convert numbers between any base with any printable character sets.
#Created date: 05/01/2021
import math
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
        raise ValueError("Base values exceed 86 symbol limit")
    if (checkSet(inputSetFull) or checkSet(outputSetFull)) is True:
        raise ValueError("Input or Output set is not unique")
    if places < 0 or places > 24:
        raise ValueError("Decimal places input is invalid")

#Correct for input errors.
def inputCorrection(input, inputBase, inputSetFull):
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
    else: 
        absPosList = posList
        floatInput = False
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
    else: 
        intPosList = inputPosList
        floatInput = False
    decimalList = map(lambda point: 
                  (inputBase ** point[0]) * point[1], enumerate(intPosList))
    if not floatInput:
        return sum(decimalList)
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
        inputQuotient = quotient * math.pow(outputBase, places)
    else: inputQuotient = quotient
    if outputBase == 1: return [0] * inputQuotient
    if inputQuotient == 0: return remainder
    newQuotient, newRemainder = divmod(inputQuotient, outputBase)
    return outputBaseConvert(outputBase, newQuotient, places, 
                             [newRemainder] + remainder)

#Convert number base with error checking.
def baseConvert(inputString:str, inputBase:int, outputBase:int = 10, places:int = 2,
                inputSetFull:str = charSet, outputSetFull:str = charSet):
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
    decimalInput = decimalConvert(inputSet, inputBase, charSet, 
                                  correctInput, inputPositionList)
    outputPositionList = outputBaseConvert(outputBase, decimalInput, places)
    return substituteChar(outputSet, outputPositionList, negative, places, inputString)
    