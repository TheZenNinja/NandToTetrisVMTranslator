import re
class Parser(object):
    def __init__(self, lines):
        self.lines = lines
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
        return self.currentLine.split()[1]
    
    def arg2(self):
        #split current line and return [2] item
        return self.currentLine.split()[2]

