from Parser import Parser
from CodeWriter import CodeWriter

#get file name
#fileName = input("please input file name: ")
fileName = 'test.txt'

#read file
f = open(fileName, 'r')
lines = f.read().split('\n')
f.close()

#create parser
parser = Parser(lines)

#create codewriter
cWriter = CodeWriter(fileName)


outFile = open('test.asm', 'w')
outFile.write('');


while parser.hasMoreCommands():
    #check command type
    cmd = parser.commandType()
    print(cmd)
    print(parser.arg1())
    print(parser.arg2())

    if (cmd == 'push'):
        c = cWriter.WritePushPop(False, parser.arg1(), parser.arg2())
    elif cmd == 'pop':
        c = cWriter.WritePushPop(True, parser.arg1(), parser.arg2())
    elif cmd == 'comment':
        parser.advance()
        continue
    else:
        print("invalid command '", cmd, "'")


    print(c)
    outFile.write(c)
    #match cmd:
    #case cmd == 'push':
    #    cWriter.WritePushPop(False, parser.arg1(), parser.arg2())
    #    break;
    #case cmd == 'pop':
    #    cWriter.WritePushPop(True, parser.arg1(), parser.arg2())
    #    break
    #case _:
    #    print("invalid command '", cmd, "'")
    #    break
    parser.advance()
    #codewriter write
    
    #advance

outFile.close()