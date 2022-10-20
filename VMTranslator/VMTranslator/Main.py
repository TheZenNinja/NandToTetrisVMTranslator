#Team V2
#Matthew C, Noah L, Michaela H
#VM Translator
#Mod 1 Lab 3
#Translate VM code to Hack asm code
#Last Updated 10/20/22
from Parser import Parser
from CodeWriter import CodeWriter

inputFile = input("Input File Path: ")
outputFile = input("Output File Path (Optional): ")

#create parser
parser = Parser(inputFile)
#create codewriter
cWriter = CodeWriter(outputFile)

#if there is no stated output file name
if len(outputFile) < 4:
    cWriter.setFileName(inputFile)

#open file
cWriter.OpenFile()

while parser.hasMoreCommands():
    #check command type
    cmd = parser.commandType()

    #process cmd
    if (cmd == 'push'):
        cWriter.WritePushPop(False, parser.arg1(), parser.arg2())
    elif cmd == 'pop':
        cWriter.WritePushPop(True, parser.arg1(), parser.arg2())
    elif cWriter.arithDic.get(cmd) != None:
        cWriter.writeArithmetic(cmd);
    elif cmd == 'comment':
        parser.advance()
        continue
    else:
        print("invalid command '", cmd, "'")
        break;
    #advance
    parser.advance()

#close file
cWriter.CloseFile()

print(inputFile, "converted to asm")