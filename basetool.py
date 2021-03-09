##########################################################################################
# Tool to convert int/float numbers between bases 0-86 with any given character sets.
# Creation date: 05/01/2021
##########################################################################################
# 135code.com API Category Definition.
category = "tools"

# Imported Tools.
from re import search
from math import pow

# Default character set.
charSet = "".join([
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '+', '/', '~', '!', '@', '#',
    '$', '%', '^', '&', '*', ';', '=', '?', '<', '>', '[', ']', ':', '"', '{', '}', ',',
    '`'])

##########################################################################################
# Function: isSet
# inputSet: Set of characters to Test.
# Returns: Boolean is inputSet a Unique Set.
def isSet(inputSet):
    return len(inputSet) == len(set(inputSet))

# Function: valuesCheck
# Purpose: Test if Inputs Meet Requirements.
def valuesCheck(inBase, outBase, inputSet, outputSet, charSet, fracPlaces):
    if inBase < 2 or inBase > len(charSet): 
        raise ValueError("Input base is out of range")
    if outBase < 2 or outBase > len(charSet):
        raise ValueError("Output base is out of range")
    if inBase > len(inputSet) or outBase > len(outputSet):
        raise ValueError("Custom set doesn't satisfy base")
    if not isSet(inputSet):
        raise ValueError("Input set is not unique")
    if not isSet(outputSet):
        raise ValueError("Output set is not unique")
    if search("[.-]", inputSet + outputSet) is not None:
        raise ValueError("Custom set contains - or .")
    if fracPlaces < 0:
        raise ValueError("Negative fractional places value")

# Function: inputSign
# Returns: Input String with Sign Removed and Sign Boolean.
def inputSign(inString):
    if inString[0] == "-": return inString[1:], True
    return inString, False

# Function: inputPosition
# Returns: List of Integer String Index Positions in Input Set.
def inputPosition(absInString, inCutSet):
    inPosList = list(map(lambda char: inCutSet.find(char), absInString))[::-1]
    if -1 in inPosList: raise ValueError("Input characters not in input set")
    return inPosList

# Function: inputFloatSplit
# Returns: Integer Value, and if Applicable Decimal Integer and Float Boolean.
def inputFloatSplit(inputSet, inPosList):
    if (len(inputSet) - 1) in inPosList:
        intPosList = inPosList[inPosList.index(len(inputSet)-1) + 1:]
        fracPosList = reversed(inPosList[:inPosList.index(len(inputSet)-1)])
        return intPosList, fracPosList, True
    return inPosList, [], False

# Function: convertDecimal
# Returns: Decimal Integer Representation of Input Integer.
def convertDecimal(absInString, inBase, inCutSet, inPosList):
    if inCutSet == ["0123456789."]: return str(absInString)
    intPosList, fracPosList, floatInput = inputFloatSplit(inCutSet, inPosList)
    intList = map(lambda pos: (inBase**pos[0])*pos[1], enumerate(intPosList))
    if not floatInput: return sum(intList), False
    fracList = map(lambda pos: (inBase**((pos[0]*-1)-1))*pos[1], enumerate(fracPosList))
    return str(sum(intList) + sum(fracList)), True

# Function: inputDivmod
# remainder: The Left Over Output Base Going into the Quotient as Many Times as Possible.
# Returns: List of Remainder Values for Each Character Position Calculated.
def inputDivmod(inputQuotient, outBase, remainder=[]):
    quotient, remainderList = divmod(inputQuotient, outBase)
    if inputQuotient == 0: return remainder
    return inputDivmod(quotient, outBase, [int(remainderList)] + remainder)

# Function: outputPosition
# Returns: Representation of Integer in Selected Output Base.
def outputPosition(fracInString, outBase, fracPlaces):
    if "." in str(fracInString): 
        inputQuotient = float(fracInString) * pow(outBase, fracPlaces)
    else: inputQuotient = int(fracInString)
    return inputDivmod(inputQuotient, outBase)

# Function: subCharacters
# Returns: List of Output Set Characters at each Output Position Index.
def subCharacters(outPosList, outCutSet):
    return "".join(list(map(lambda pos: outCutSet[pos], outPosList)))

# Function: outputFormat
# Returns: Output Integer Correctly Formatted (Applicable Sign and/or Decimal Point).
def outputFormat(string, fracPlaces, fracInput, sign):
    if fracInput and fracPlaces != 0:
        Integer = string[:(fracPlaces*-1)]
        if not Integer: fracString = "0" + "." + string[(fracPlaces*-1):]
        else: fracString = Integer + "." + string[(fracPlaces*-1):]
    else: fracString = string
    if sign: return "-" + fracString
    return fracString

##########################################################################################
# Function: baseConvert
# inBase: The Base that the Input will be Interpreted as.
# outBase: The Base for the Input String to be Converted into.
# inputSet: The Set of Characters to Reference for Interpreting the Input.
# outputSet: The Set of Characters to Reference for Substituting the Output.
# fracPlaces: The Number of Decimal Places to Calculate for Output.
def baseConvert(inputString: str, inBase: str, outBase: str = "10",
                inputSet: str = charSet, outputSet: str = charSet, fracPlaces: str = "5"):
    # Check Integer Argument Inputs are Integers.
    try: inBaseInt, outBaseInt, fracPlacesInt = int(inBase), int(outBase), int(fracPlaces)
    except: raise ValueError("Integer arguments contain non-integer values")
    # Test Inputs for any Incorrect Arguments.
    valuesCheck(inBaseInt, outBaseInt, inputSet, outputSet, charSet, fracPlacesInt)
    # Trim Input and Output Character Sets to Length of Input and Output Bases.
    inCutSet = inputSet[0:inBase] + "."
    outCutSet = outputSet[0:outBase] + "."
    # Check and Store if Input is Positive or Negative.
    absInString, sign = inputSign(inputString)
    # Index all Character Inputs against Input Character Set.
    inPosList = inputPosition(absInString, inCutSet)
    # Convert Input Number from Input Base to Decimal (Base10).
    fracInString, fracInput = convertDecimal(absInString, inBaseInt, inCutSet, inPosList)
    # Convert Calculated Decimal Number to the Correct Output Base.
    outPosList = outputPosition(fracInString, outBaseInt, fracPlacesInt)
    # Substitute Output Index Values for Output Character Set Values.
    outputString = subCharacters(outPosList, outCutSet)
    # Correctly Format Output (sign, decimal point).
    return outputFormat(outputString, fracPlacesInt, fracInput, sign)

##########################################################################################
# Expose baseConvert to the API as convert
API_convert = baseConvert