#Team V2
#Matthew C, Noah L, Michaela H
#VM Translator - Code Writer
#Mod 1 Lab 3
#Takes generalized commands and converts them into Hack asm code
#Last Updated 10/20/22
import re
class CodeWriter(object):
    segStackP   = 0
    segLcl      = 1
    segArg      = 2
    segPoint    = 3
    segTemp     = 5
    segStatic   = 16
    segStack    = 256 #-2047

    pushDict = {
        'default'   : "//--push {memSeg} {loc}--\n//get {memSeg} {loc}\n@{loc}\nD=A\n@{addrLoc}\nA=D+M\nD=M\n//push to stack\n@0\nA=M\nM=D\n\n",
        'constant'  : "//--push constant {loc}--\n//get constant {loc}\n@{addr}\nD=A\n//push to stack\n@0\nA=M\nM=D\n\n",
        'pointer'   : "//--push pointer {loc}\n@{addr}\nD=M\n//push to stack\n@0\nA=M\nM=D\n",
        'temp'      : "//--push temp {loc}\n@{addr}\nD=M\n//push to stack\n@0\nA=M\nM=D\n\n"
        }
    popDict = {
        'default'   : "//--pop {memSeg} {loc}--\n//get addr {memSeg} {loc}\n@{loc}\nD=A\n@{addrLoc}\nD=D+M\n//save location to gen reg \n@13\nM=D\n//get value from stack, accounting for the moved pointer\n@0\nA=M\nD=M\n//move back to stored value\n@13\nA=M\nM=D\n//clear stack value\n@0\nA=M\nM=0\n//clear gen reg value\n@13\nM=0\n\n",
        'pointer'   : "//--pop pointer {loc}--\n//get addr pointer {loc}\n@{addrLoc}\nD=A\n//save location to gen reg\n@13\nM=D\n//get value from stack, accounting for the moved pointer\n@0\nA=M\nD=M\n//move back to stored value\n@13\nA=M\nM=D\n//clear stack value\n@0\nA=M\nM=0\n//clear gen reg value\n@13\nM=0\n",
        'temp'      : "//--pop temp {loc}--\n//get addr temp {loc}\n@{addr}\nD=A\n//save location to gen reg\n@13\nM=D\n//get value from stack, accounting for the moved pointer\n@0\nA=M\nD=M\n//move back to stored value\n@13\nA=M\nM=D\n//clear stack value\n@0\nA=M\nM=0\n//clear gen reg value\n@13\nM=0\n",
        }
    arithDic = {
        'add'   : "//--add--\n//decr sp\n@0\nM=M-1\n//go to stack and save to reg and clear\nA=M\nD=M\nM=0\n//go to lower stack location and add to it\n@0\nA=M-1\nM=M+D\n",
        'sub'   : "//--sub--\n//dec sp\n@0\nM=M-1\n//go to stack and save to reg and clear\nA=M\nD=M\nM=0\n//go to lower stack addr and sub to it\n@0\nA=M-1\nM=M-D\n",
        'neg'   : "//--neg--\n@0\n//load 0 into reg\nD=A\n//go to stack addr\nA=M-1\n//sub 0 from the value in mem\nM=D-M\n",
        'eq'    : "//--eq--\n//dec sp and go to stack\n@0\nM=M-1\nA=M\n//get top stack val and clear it\nD=M\nM=0\n//go to next stack val\n@0\nA=M-1\n//sub from eachother to check if ==\nD=D-M\n//jump to true if they are the same\n@TRUE_X\nD;JEQ\n//false\n@0\nA=M-1\nM=0\n@END_X\n0;JMP\n//true\n(TRUE_X)\n@0\nA=M-1\nM=1\n//the end of branch\n(END_X)\n",
        'gt'    : "//greater than\n@0\nM=M-1\nA=M\nD=M\n@13\nM=D\n@0\nM=M-1\nA=M\nD=M\n@13\nD=D-M\n@TRUE_X\nD;JGT\n@13\nM=0\nD=0\n@PUSH_X\n0;JMP\n(TRUE_X)\n@13\nM=0\nD=1\n(PUSH_X)\n@0\nA=M\nM=D\n@0\nM=M+1\n",
        'lt'    : "//less than\n@0\nM=M-1\nA=M\nD=M\n@13\nM=D\n@0\nM=M-1\nA=M\nD=M\n@13\nD=D-M\n@TRUE_X\nD;JLT\n@13\nM=0\nD=0\n@PUSH_X\n0;JMP\n(TRUE_X)\n@13\nM=0\nD=1\n(PUSH_X)\n@0\nA=M\nM=D\n@0\nM=M+1\n",
        'and'   : "//--and--\n//decrement stack pointer and save to D then clear\n@0\nM=M-1\nA=M\nD=M\n//store val in r13\n@13\nM=D\n//retrieve 2nd value and store in D then clear\n@0\nM=M-1\nA=M\nD=M\n//compare values using and, save in D\n@13\nD=D&M\n//clear r13\nM=0\n//increment pointer and push D to stack\n@0\nM=M+1\nA=M-1\nM=D\n",
        'or'    : "//--Or--\n//decrement stack pointer and save to D then clear\n@0\nM=M-1\nA=M\nD=M\n//store val in r13\n@13\nM=D\n//retrieve 2nd value and store in D then clear\n@0\nM=M-1\nA=M\nD=M\n//compare values using or, save in D\n@13\nD=D|M\n//clear r13\nM=0\n//increment pointer and push D to stack\n@0\nM=M+1\nA=M-1\nM=D\n",
        'not'   : "//--not--\n//go to top value in the stack and save in D\n@0\nA=M-1\nD=M\n//negate D and push to stack\n//If 0, make 1. If 1, make 0\n@ISZERO_X\nD;JEQ\n//its one, make it zero\nD=0\n@PUSH_X\n0; JMP\n(ISZERO_X)\n//its zero, so make it one\nD=1\n(PUSH_X)\n//now push to stack\n@0\nA=M-1\nM=D\n"
        }


    def __init__(self, outputFilePath):
        self.outputFilePath = outputFilePath
        self.labelIndex = 0;

    def setFileName(self, fileName):
        self.outputFilePath = re.sub('\..{1,4}$','.asm',fileName)
        #self.outputFilePath = fileName[:-2] + ".asm"
    
    def writeArithmetic(self, cmd):
        pattern = self.arithDic.get(cmd, "-----ERROR-----")
        pattern = pattern.replace("_X", "_" + str(self.labelIndex))
        if cmd == 'eq' or cmd == 'gt' or cmd == 'lt' or cmd == 'not':
            self.labelIndex = self.labelIndex + 1;

        self.outputFile.write(pattern)
    
    def WritePushPop(self, isPop, memSeg, loc):
        pattern = '';

        baseAddr = 0;
        if memSeg == 'local':
            baseAddr = self.segLcl
        elif memSeg == 'argument':
            baseAddr = self.segArg
        elif memSeg == 'pointer':
            baseAddr = self.segPoint
        elif memSeg == 'temp':
            baseAddr = self.segTemp
        elif memSeg == 'static':
            baseAddr = self.segStatic

        #Pop
        if isPop:
            if memSeg == 'constant':
                print('Error: cant pop to constant')
                return
            #decrement stack pointer
            pattern = "//decr stack pointer\n@0\nM=M-1\n\n"

            pattern = pattern + self.popDict.get(memSeg, self.popDict['default'])

            pattern = pattern.replace('{loc}', str(loc))
            pattern = pattern.replace('{memSeg}', str(memSeg))

            if memSeg == 'pointer' or memSeg == 'temp':
                pattern = pattern.replace('{addr}', str(baseAddr + int(loc)))
            else:
                pattern = pattern.replace('{addrLoc}', str(baseAddr))
        #Push
        else:
            pattern = self.pushDict.get(memSeg, self.pushDict['default'])

            #replacing the values in the string
            pattern = pattern.replace('{loc}', str(loc))
            pattern = pattern.replace('{memSeg}', str(memSeg))

            #if memSeg == 'pointer' or memSeg == 'temp':
            pattern = pattern.replace('{addr}', str(baseAddr + int(loc)))
            #else:
            pattern = pattern.replace('{addrLoc}', str(baseAddr))

            #increment stack pointer
            pattern = pattern + "//incr stack pointer\n@0\nM=M+1\n\n"

        self.outputFile.write(pattern)
    
    def OpenFile(self):
        self.outputFile = open(self.outputFilePath, 'w')

    def CloseFile(self):
        self.outputFile.write("\n\n(END_OF_PROGRAM)\n@END_OF_PROGRAM\n0;JMP")
        self.outputFile.close()


