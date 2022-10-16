class CodeWriter(object):
    segStackP   = 0
    segLcl      = 1
    segArg      = 2
    segPoint    = 3
    segTemp     = 5
    segStatic   = 16
    segStack    = 256 #-2047

    pushDict = {
        'default' : "//--push {memSeg} {loc}--\n//get {memSeg} {loc}\n@{loc}\nD=A\n@{addrLoc}\nA=D+M\nD=M\n//push to stack\n@0\nA=M\nM=D\n\n",
        'constant': "//--push constant {loc}--\n//get constant {loc}\n@{addr}\nD=A\n//push to stack\n@0\nA=M\nM=D\n\n",
        'pointer': "//--push pointer {loc}\n@{addr}\nD=M\n//push to stack\n@0\nA=M\nM=D\n",
        'temp': "//--push temp {loc}\n@{addr}\nD=M\n//push to stack\n@0\nA=M\nM=D\n\n"
        }
    popDict = {
        'default': "//--pop {memSeg} {loc}--\n//get addr {memSeg} {loc}\n@{loc}\nD=A\n@{addrLoc}\nD=D+M\n//save location to gen reg \n@13\nM=D\n//get value from stack, accounting for the moved pointer\n@0\nA=M\nD=M\n//move back to stored value\n@13\nA=M\nM=D\n//clear stack value\n@0\nA=M\nM=0\n//clear gen reg value\n@13\nM=0\n\n",
        'pointer': "//--pop pointer {loc}--\n//get addr pointer {loc}\n@{addrLoc}\nD=A\n//save location to gen reg\n@13\nM=D\n//get value from stack, accounting for the moved pointer\n@0\nA=M\nD=M\n//move back to stored value\n@13\nA=M\nM=D\n//clear stack value\n@0\nA=M\nM=0\n//clear gen reg value\n@13\nM=0\n",
        'temp': "//--pop temp {loc}--\n//get addr temp {loc}\n@{addr}\nD=A\n//save location to gen reg\n@13\nM=D\n//get value from stack, accounting for the moved pointer\n@0\nA=M\nD=M\n//move back to stored value\n@13\nA=M\nM=D\n//clear stack value\n@0\nA=M\nM=0\n//clear gen reg value\n@13\nM=0\n",
        }


    def __init__(self, path):
        self.setFileName(path)

    #read file, write file, or both?
    def setFileName(self, path):
        self.outputFile = path[:-2] + "asm"
    
    def writeArithmetic(self):
        #matt: add sub neg
        #eq get let
        #and or not

        #switch on the operator and then ad/sub/mult using patterns on the top 2 numbers in the stack
            #if +/-
                #get the first number and store it in reg
                #m=m+/-D
            #if *
                #do the whole * thing using the temp mem-seg
        return
    
    #dont forget to add segBase + the value 
   


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
        else:
            pattern = self.pushDict.get(memSeg, self.pushDict['default'])

            #getting the memAddr from the local addr
            

            #replacing the values in the string
            pattern = pattern.replace('{loc}', str(loc))
            pattern = pattern.replace('{memSeg}', str(memSeg))

            #if memSeg == 'pointer' or memSeg == 'temp':
            pattern = pattern.replace('{addr}', str(baseAddr + int(loc)))
            #else:
            pattern = pattern.replace('{addrLoc}', str(baseAddr))

            #increment stack pointer
            pattern = pattern + "//incr stack pointer\n@0\nM=M+1\n\n"

        return pattern
        #if isPop
            #use pop pattern
        #else
            #use push pattern

        #create list of commands (and comment) with the selected regex
        #write to file
        



