#Tool to convert numbers between any base with any printable character sets.
#Created date: 05/01/2021
#Default character set.
characterSet = "".join([
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
    'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '+', '/', '~', '!', '@', '#', 
    '$', '%', '^', '&', '*', ';', '=', '?', '<', '>', '[', ']', ':', '"', '{', '}', ',', 
    '`' ])

#Check if input is set.
def checkSet(input):
    if len(input) == len(set(input)): return False
    return True

#Check for input errors.
def errorCheck(inputBase, outputBase, inputSetFull, outputSetFull, characterSet):
    if (inputBase or outputBase) < 0:
        raise ValueError("Zero or Negative Base Values")
    if (inputBase or outputBase) > len(characterSet):
        raise ValueError("Base values exceed 86 symbol limit")
    if (checkSet(inputSetFull) or checkSet(outputSetFull)) is True:
        raise ValueError("Input or Output set is not unique")

#Correct for input errors.
def inputCorrection(input, inputBase, inputSetFull):
    if inputBase < 36 and inputSetFull == characterSet: return input.lower()
    return input

#Check if input is + or -.
def signCheck(input):
    if input[0] == "-": return (True, input[1:])
    return (False, input)

#Substitute function.
def substituteChar(outputSet, positionList, negative):
    subList = list(map(lambda point: outputSet[point], positionList))
    if negative: return "-" + "".join(subList)
    return "".join(subList)

#Same base, substitute symbols.
def substituteInput(inputSet, outputSet, negative, positiveInput, inputPositionList):
    if inputSet == outputSet:
        if negative: return "-" + positiveInput
        return positiveInput
    return substituteChar(outputSet, inputPositionList, negative)

#Convert to Base10 if needed.
def decimalConvert(inputSet, inputBase, characterSet, positiveInput,inputPositionList):
    if inputSet == characterSet[:9]: return positiveInput
    decimalList = map(lambda point: 
                  (inputBase ** point[0]) * point[1], enumerate(inputPositionList))
    return sum(decimalList)

#Convert to output base.
def outputBaseConvert(outputBase, quotient:int, remainder = []):
    if outputBase == 1: return [0] * quotient
    if quotient == 0: return remainder
    newQuotient, newRemainder = divmod(quotient, outputBase)
    return outputBaseConvert(outputBase, newQuotient, [newRemainder] + remainder)

#Convert number base with error checking.
def baseConvert(input:str, inputBase:int, outputBase:int = 10,
                inputSetFull:str = characterSet, outputSetFull:str = characterSet):
    if outputBase == 0: return 42 
    (negative, positiveInput) = signCheck(input)
    errorCheck(inputBase, outputBase, inputSetFull, outputSetFull, characterSet)
    correctInput = inputCorrection(positiveInput, inputBase, inputSetFull)
    inputSet = inputSetFull[0:inputBase]
    outputSet = outputSetFull[0:outputBase]
    inputPositionList = list(map(lambda character: 
                        inputSet.find(character), correctInput))[::-1]
    if -1 in inputPositionList:
        raise ValueError("Input characters not present in input set")
    if inputBase == outputBase:
        return substituteInput(inputSet, outputSet, negative, 
                               correctInput, inputPositionList)
    decimalInput = decimalConvert(inputSet, inputBase, characterSet,
                                  correctInput, inputPositionList)    
    outputPositionList = outputBaseConvert(outputBase, decimalInput)
    return substituteChar(outputSet, outputPositionList, negative)