#Team V2
#Matthew C, Noah L, Michaela H
#VM Translator - Parser
#Mod 1 Lab 3
#Reads input file and seperates VM commands into components
#Last Updated 10/20/22
import re
class Parser(object):
    def __init__(self, inputFileName):
        f = open(inputFileName, 'r')
        self.lines = f.read().split('\n')
        f.close()

        self.lineNum = -1;
        self.currentLine = '';
        self.advance()
        #todo remove any lines that start with //
        self.lines

    def hasMoreCommands(self):
        return self.lineNum < len(self.lines)
    
    def advance(self):
        self.lineNum = self.lineNum + 1
        if self.hasMoreCommands():
            self.currentLine = self.lines[self.lineNum]
    
    def commandType(self):
        #return an id string based on the split current line [0] item
        cmd = self.currentLine.split()[0]
        if re.match('^//.*', cmd):
            return 'comment'
        else:
            return cmd
    
    def arg1(self):
        #split current line and return [1] item
        a = self.currentLine.split()
        if len(a) > 1:
            return a[1]
        else:
            return "error"
    
    def arg2(self):
        #split current line and return [2] item
        a = self.currentLine.split()
        if len(a) > 2:
            return a[2]
        else:
            return "error"

