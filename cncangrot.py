#!/usr/bin/env python2.7

## [ CNCANGROT.PY ]-------------------------------------------------------------+
## CNC Angular Rotation utility that provides a simple means of translating     |
## G-code files based on a rotation axis about the defined origin.              |
##                                                                              |
## Mathematic formulae;                                                         |
## p'x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox                       |
## p'y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy                       |
## p(initial point) -> p'(new point) about o(origin) at theta(anglular rotation)|
## -----------------------------------------------------------------------------+
## Written by John P. Lettman 4/16/2012

"""CNC Angular Rotation utility that provides a simple means of translating
G-code files based on a rotation axis about the defined origin."""

## Module documentation.
__author__ = "John P. Lettman"
__version__ = "0.0.2"
__maintainer__ = "John P. Lettman"
__email__ = "JohnL@seitz.com"
__status__ = "Development"

CRLF = "\r\n" # DOS

import math
from time import gmtime, strftime

def printOut(message, error=False):
    global args
    timestamp = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
    if not error: 
        if args.verbose: print("[" + timestamp + "] INFO // " + str(message))
    else: print("[" + timestamp + "] ERROR! // " + str(message))


def angularTranslate(inputFileLocation, outputFileLocation, pivot = (0, 0)):
    from decimal import Decimal # We need this for precision.
    
    # Assign the appropiate variables with pivot.
    lastXYTranslated = lastXY = pivotX, pivotY = pivot
    
    newGcode = []
    __lineNum = 1
    
    with open(inputFileLocation, "r") as inputFile:
        ## We have opened the input file,
        ## now we're going to iterate over
        ## every single line!
        
        for line in inputFile:
            printOut("Interpretting line " + str(__lineNum))
            currentLine = line.lstrip()
            
            
            if currentLine == "" or currentLine.isspace(): 
                newGcode.append([""])
                __lineNum += 1
                continue
            else: 
                newGcode.append([])
            
            __currentLineSplit = currentLine.split(" ")
            __pos = 0
            
            if __currentLineSplit[0] == "G90":
                newGcode[__lineNum-1].append("G90")

            elif __currentLineSplit[0] == "G91": # no G91 please ):
                #printOut("This program does not interpret G91s!", True)
                #sys.exit(1)
                newGcode[__lineNum-1].append("G91")
                    
            elif __currentLineSplit[0].startswith(";") or __currentLineSplit[0] == ";":
                ## Oh look, comments!
                printOut("Encountered a commented line at " + str(__lineNum))
                newGcode[__lineNum-1].append(currentLine)
                __lineNum += 1
                continue
            

            ## G-codes that need to be translated.
            elif __currentLineSplit[0] == "G00" or __currentLineSplit[0] == "G01": # RAPID / STRAIGHT
                x, y = __currentLineSplit[1:3]
                
                
                ## Sanity check for coordinates.
                
                try: # Convert x to decimal...
                    px = Decimal(x[1:])
                    xFailed = False
                except:
                    ## We couldn't convert it
                    xFailed = True
                
                try: # Convert y to decimal...  
                    py = Decimal(y[1:])
                    yFailed = False
                except:
                    ## We couldn't convert it
                    yFailed = True
                
                if xFailed or x.upper()[0] != "X":
                    printOut("X value at line " + str(__lineNum) + "is malformed!", True)
                    sys.exit(1)
                    
                if yFailed or y.upper()[0] != "Y":
                    printOut("Y value at line " + str(__lineNum) + "is malformed!", True)
                    sys.exit(1)
                    
                    
                ## Convert!
                nx = Decimal(Decimal(math.cos(args.angle)) * (px - pivotX) - Decimal(math.sin(args.angle)) * (py - pivotY) + pivotX)
                ny = Decimal(Decimal(math.sin(args.angle)) * (px - pivotX) + Decimal(math.cos(args.angle)) * (py - pivotY) + pivotY) 
                
                newGcode[__lineNum-1].append(__currentLineSplit[0])
                newGcode[__lineNum-1].append("X" + str(round(nx, 3)))
                newGcode[__lineNum-1].append("Y" + str(round(ny, 3)))
                
                lastXY = (px, py)
                lastXYTranslated = (nx, ny)
                    
                __pos += 2 # move up the stack
                
            elif __currentLineSplit[0] == "G02" or __currentLineSplit[0] == "G03": # CW / CCW
                x, y, i, j = __currentLineSplit[1:5]
                    
                ## Sanity check for coordinates.
                
                try:
                    px = Decimal(x[1:])
                    xFailed = False
                except:
                    xFailed = True
                
                try:
                    py = Decimal(y[1:])
                    yFailed = False
                except:
                    yFailed = True
                    
                try:
                    pi = Decimal(i[1:])
                    iFailed = False
                except:
                    iFailed = True
                
                try:
                    pj = Decimal(j[1:])
                    jFailed = False
                except:
                    jFailed = True
                
                if xFailed or x.upper()[0] != "X":
                    printOut("X value at line " + str(__lineNum) + "is malformed!", True)
                    sys.exit(1)
                    
                if yFailed or y.upper()[0] != "Y":
                    printOut("Y value at line " + str(__lineNum) + "is malformed!", True)
                    sys.exit(1)   
                    
                if iFailed or i.upper()[0] != "I":
                    printOut("I value at line " + str(__lineNum) + "is malformed!", True)
                    sys.exit(1)
                    
                if jFailed or j.upper()[0] != "J":
                    printOut("J value at line " + str(__lineNum) + "is malformed!", True)
                    sys.exit(1)
                    
                lastRadiusX = lastXY[0] + pi
                lastRadiusY = lastXY[1] + pj
                
                newRadiusX = Decimal(Decimal(math.cos(args.angle)) * (lastRadiusX - pivotX) \
                                     - Decimal(math.sin(args.angle)) * (lastRadiusY - pivotY) + pivotX)
                
                newRadiusY = Decimal(Decimal(math.sin(args.angle)) * (lastRadiusX - pivotX) \
                                     + Decimal(math.cos(args.angle)) * (lastRadiusY - pivotY) + pivotY)   
                    
                nx = Decimal(Decimal(math.cos(args.angle)) * (px - pivotX) - Decimal(math.sin(args.angle)) * (py - pivotY) + pivotX)
                ny = Decimal(Decimal(math.sin(args.angle)) * (px - pivotX) + Decimal(math.cos(args.angle)) * (py - pivotY) + pivotY)
                
                ni = newRadiusX - lastXYTranslated[0]
                nj = newRadiusY - lastXYTranslated[1]
                
                newGcode[__lineNum-1].append(__currentLineSplit[0])
                newGcode[__lineNum-1].append("X" + str(round(nx, 3)))
                newGcode[__lineNum-1].append("Y" + str(round(ny, 3)))
                newGcode[__lineNum-1].append("I" + str(round(ni, 3)))
                newGcode[__lineNum-1].append("J" + str(round(nj, 3)))
                    
                lastXY = (px, py)
                lastXYTranslated = (nx, ny)
                    
                __pos += 4
                    
            else:
                printOut("Unexpected code, moving on...")
                newGcode[__lineNum-1].append(currentLine)
                __lineNum += 1
                continue
            
            
            ## Attach comments
            newGcode[__lineNum-1].append(" ".join(__currentLineSplit[1+__pos:]))
            
            ## line++        
            __lineNum += 1
            
    ## END OF LOOP! Write to file!
    printOut("Writing to file: '" + outputFileLocation + "'")
    
    ## Open as 'wb' or 'write binary' for CRLFs
    with open(outputFileLocation, "wb") as outputFile:
        for line in newGcode: 
            lineCompiled = " ".join(line).strip() + CRLF
            printOut(lineCompiled)
            outputFile.write(lineCompiled)
        
    # Done!
            
## Do execution if we are not a 'include'.
if __name__ == "__main__":
    import os
    import sys
    import argparse
    
    ## Create an argument parsing instance...
    parser = argparse.ArgumentParser(description=__doc__, prog=os.path.basename(__file__),
                                     epilog="Written by " + __author__ + " | may contain peanuts")
    
    ## Add command line arguments to interpret...
    parser.add_argument("angle", type=float, help="angle to rotate by (degrees unless --radians)")
    parser.add_argument("infile", type=str, help="g-code file to translate")
    parser.add_argument("outfile", type=str, help="output of translated g-code")
    parser.add_argument("--radians", action="store_true", help="set angle as radians")
    parser.add_argument("--use-same-file", action="store_true", help="ignore 'same file' warning")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("-v", "--verbose", action="store_true", help="show debug information")
    
    ## Parse them! (and sanitize)
    args = parser.parse_args()
    
    inputFile = os.path.normpath(args.infile)
    outputFile = os.path.normpath(args.outfile)
    if not args.radians: args.angle = math.radians(args.angle)
    
    ## Sanity check - does our file exist/is it the same?
    if not os.path.exists(inputFile):
        printOut("File: '" + os.path.basename(inputFile) + "' does not exist!", True)
        sys.exit(1)
        
    if (inputFile == outputFile) and (not args.use_same_file):
        printOut("Files: '" + os.path.basename(inputFile) + "' and '" + os.path.basename(inputFile) + "'" +
                 "are the same files!\n\nAppend the option --use-same-file to ignore this error.", True)
        sys.exit(1)
        
    
    angularTranslate(inputFile, outputFile)