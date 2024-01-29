import os

# A commands
A_ASSIGN_M = "A=M"
A_ADD_D_TO_M = "A=M+D"
A_ASSIGN_D = "A=D"

# D commands
D_ASSIGN_A = "D=A"
D_ASSIGN_M = "D=M"
D_SUBTRACT_D_FROM_M = "D=M-D"
D_SUBTRACT_M_FROM_D = "D=D-M"
D_ADD_M_TO_D = "D=D+M"
D_SUBTRACT_A_FROM_D = "D=D-A"
D_ADD_A_TO_D = "D=D+A"

# M commands
M_DECREMENT = "M=M-1"
M_INCREMENT = "M=M+1"
M_SET_ZERO = "M=0"
M_INVERT_SIGN = "M=-M"
M_LOGICAL_NOT = "M=!M"
M_SET_NEGATIVE_ONE = "M=-1"
M_ASSIGN_D = "M=D"
M_ADD_D = "M=M+D"
M_SUBTRACT_D = "M=M-D"
M_BITWISE_AND_D = "M=M&D"
M_BITWISE_OR_D = "M=M|D"

#Jump commands
JMP = "0;JMP"
JEQ = "D;JEQ"
JGT = "D;JGT"
JGE = "D;JGE"
JLT = "D;JLT"
JLE = "D;JLE"
JNE = "D;JNE"

LABEL = "(%s)"
IF_GOTO = "if-false-goto %s"

# symbol
AT = "@"
SPINDEX = "256"
ATSP = "@SP"
TEMP = "13"
ATFUNC = "@FUNC"
FALSE = "(FALSE"
TRUE = "(TRUE"
FUNC = "(FUNC"

class CodeWriter:
    ramSymbol_dict = {
        "SP": "0",
        "local": "1",
        "argument": "2",
        "this": "3",
        "that": "4",
        "temp": "5",
        "pointer": "3",
        "static" : "16",
    }
    
    def __init__(self, file_path):
        self.outputFile = open(file_path, 'w')
        self.booleanCounter = 0
        self.baseFilename = os.path.basename(file_path).split('.')[0]
        self.returnAddressCounter = 0
        self.curFunc = ""
        self.curFile = ""


    def writeArithmetic(self, c_type):
        if c_type == "add":
            self.add()
            return
        elif c_type == "sub":
            self.sub()
            return
        elif c_type == "neg":
            self.neg()
            return
        elif c_type == "not":
            self.nott()
            return
        elif c_type == "and":
            self.andd()
            return
        elif c_type == "or":
            self.orr()
            return
        elif c_type == "eq":
            self.eq()
        elif c_type == "gt":
            self.gt()
        elif c_type == "lt":
            self.lt()
        #self.writeFalse()
        #self.writeTrue()
        #self.writeFunc()
        #self.booleanCounter += 1

    def popFromStackToD(self):
        asmLines = []
        asmLines.append(ATSP)
        asmLines.append(M_DECREMENT)
        asmLines.append(A_ASSIGN_M)
        asmLines.append(D_ASSIGN_M)
        self.writeAsmLines(asmLines)

    def popFromStackToNone(self):
        asmLines = []
        asmLines.append(ATSP)
        asmLines.append(M_DECREMENT)
        asmLines.append(A_ASSIGN_M)
        self.writeAsmLines(asmLines)

    def add(self):
        asmLines = []
        self.popFromStackToD()
        self.popFromStackToNone()
        asmLines.append(M_ADD_D)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)

    def sub(self):
        asmLines = []
        self.popFromStackToD()
        self.popFromStackToNone()
        asmLines.append(M_SUBTRACT_D)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)
    
    def neg(self):
        asmLines = []
        self.popFromStackToNone()
        asmLines.append(M_INVERT_SIGN)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)

    def nott(self):
        asmLines = []
        self.popFromStackToNone()
        asmLines.append(M_LOGICAL_NOT)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)

    def andd(self):
        asmLines = []
        self.popFromStackToD()
        self.popFromStackToNone()
        asmLines.append(M_BITWISE_AND_D)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)

    def orr(self):
        asmLines = []
        self.popFromStackToD()
        self.popFromStackToNone()
        asmLines.append(M_BITWISE_OR_D)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)


    def eq(self):
        self.booleanCounter += 1
        self.comparison()
        asmLines = self.constructComparison(JEQ)
        self.pushResultToStack(asmLines)

    def gt(self):
        self.booleanCounter += 1
        self.comparison()
        asmLines = self.constructComparison(JGT)
        self.pushResultToStack(asmLines)

    def lt(self):
        self.booleanCounter += 1
        self.comparison()
        asmLines = self.constructComparison(JLT)
        self.pushResultToStack(asmLines)

    def comparison(self):
        self.popFromStackToD()
        asmLines = [ATSP, M_DECREMENT, A_ASSIGN_M, D_SUBTRACT_D_FROM_M]
        self.writeAsmLines(asmLines)

    def constructComparison(self, jumpCommand):
        labelTrue = f"TRUE{self.booleanCounter}"
        labelFalse = f"FALSE{self.booleanCounter}"
        labelEnd = f"END{self.booleanCounter}"
        return [
            f"@{labelTrue}", jumpCommand, 
            f"@{labelFalse}", JMP, 
            f"({labelTrue})", "D=-1", 
            f"@{labelEnd}", JMP, 
            f"({labelFalse})", "D=0", 
            f"({labelEnd})"
        ]

    def pushResultToStack(self, asmLines):
        asmLines.extend([ATSP, A_ASSIGN_M, M_ASSIGN_D, ATSP, M_INCREMENT])
        self.writeAsmLines(asmLines)

    def writePushPop(self, c_type, segment, index):
        if c_type == "C_PUSH":
            self.writePush(segment, index)
        else:
            self.writePop(segment, index)

    def writePop(self, segment, index):
        asmLines = [ATSP, M_DECREMENT, A_ASSIGN_M, D_ASSIGN_M]
        if segment in ["temp", "pointer"]:
            address = str(int(self.ramSymbol_dict[segment]) + int(index))
            asmLines.extend([AT + address, M_ASSIGN_D])
        elif segment == "static":
            static_address = self.curFile.replace(".vm", "") + "." + str(index)
            asmLines.extend([AT + static_address, M_ASSIGN_D])
        else:  
            asmLines.extend([
                AT + str(self.ramSymbol_dict[segment]), D_ASSIGN_M,
                AT + str(index), D_ADD_A_TO_D,
                AT +"R"+ TEMP, M_ASSIGN_D, 
                ATSP, A_ASSIGN_M, D_ASSIGN_M,
                AT +"R"+ TEMP, A_ASSIGN_M, M_ASSIGN_D
            ])
        self.writeAsmLines(asmLines)

    def writePush(self, segment, index):
        asmLines = []
        if segment == "constant":
            asmLines.extend([AT + str(index), D_ASSIGN_A])
        elif segment in ["temp", "pointer"]:
            address = str(int(self.ramSymbol_dict[segment]) + int(index))
            asmLines.extend([AT + address, D_ASSIGN_M])
        elif segment == "static":
            static_address = self.curFile.replace(".vm", "") + "." + str(index)
            asmLines.extend([AT + static_address,  D_ASSIGN_M])
        else: 
            asmLines.extend([
                AT + str(self.ramSymbol_dict[segment]),  D_ASSIGN_M,
                AT + str(index), D_ADD_A_TO_D,
                A_ASSIGN_D,  D_ASSIGN_M
            ])
        asmLines.extend([ATSP, A_ASSIGN_M, M_ASSIGN_D, ATSP, M_INCREMENT])
        self.writeAsmLines(asmLines)

    def pushTOStackFromD(self):
        asmLines = []
        asmLines.append(ATSP)
        asmLines.append(A_ASSIGN_M)
        asmLines.append(M_ASSIGN_D)
        asmLines.append(ATSP)
        asmLines.append(M_INCREMENT)
        self.writeAsmLines(asmLines)
        
    
    def popFromStackToDEST(self):
        asmLines = []
        asmLines.append(ATSP)
        asmLines.append(M_DECREMENT)
        asmLines.append(A_ASSIGN_M)
        asmLines.append(D_ASSIGN_M)
        asmLines.append(AT+TEMP)
        asmLines.append(A_ASSIGN_M)
        asmLines.append(M_ASSIGN_D)
        self.writeAsmLines(asmLines)

    
    def readFromAddress(self, address):
        asmLines = []
        asmLines.append(AT + str(address))
        asmLines.append(D_ASSIGN_M)
        self.writeAsmLines(asmLines)

    def readFromA(self, address):
        asmLines = []
        asmLines.append(AT + str(address))
        asmLines.append(D_ASSIGN_A)
        self.writeAsmLines(asmLines)
    
    def writeAsmLines(self, asmLines):
        for line in asmLines:
            self.outputFile.write(line + "\n")

    def writeLabel(self, labelName):
        name = self.curFunc + ":" + labelName
        full_label = LABEL % name
        self.writeAsmLines([full_label])


    def writeGOTO(self, destination):
        asmLines = []
        name = self.curFunc + ":" + destination
        asmLines = [AT + name, JMP]
        self.writeAsmLines(asmLines)

    def writeIf(self, destination):
        asmLines = []
        self.popFromStackToD()
        name = self.curFunc + ":" + destination
        asmLines.extend([AT + name, JNE])
        self.writeAsmLines(asmLines)     

    def writeFuncation(self, functionName, numOfLocals):
        self.curFunc = functionName
        self.writeAsmLines([LABEL % functionName])
        for i in range(int(numOfLocals)):
            self.writePush("constant", 0)


    def writeCall(self, functionName, numOfArgs):
        asmLines = []
        self.writePush("constant", "RETURN_ADDRESS" + str(self.returnAddressCounter))
        self.pushFrame("local")
        self.pushFrame("argument")
        self.pushFrame("this")
        self.pushFrame("that")

        asmLines = [ATSP, D_ASSIGN_M, AT + numOfArgs, D_SUBTRACT_A_FROM_D, AT + "5", D_SUBTRACT_A_FROM_D, AT + self.ramSymbol_dict["argument"], M_ASSIGN_D]
        self.writeAsmLines(asmLines)

        asmLines = [ATSP, D_ASSIGN_M, AT + self.ramSymbol_dict["local"], M_ASSIGN_D]
        self.writeAsmLines(asmLines)

        self.writeAsmLines([AT + functionName, JMP])
        self.writeAsmLines([LABEL % ("RETURN_ADDRESS" + str(self.returnAddressCounter))])
        self.returnAddressCounter += 1

    def pushFrame(self, segment):
        asmLines = []
        asmLines = [AT + self.ramSymbol_dict[segment], D_ASSIGN_M]
        self.writeAsmLines(asmLines)
        self.pushTOStackFromD()  

    def writeReturn(self):
        asmLines = [AT + "LCL", D_ASSIGN_M, AT + "frame", M_ASSIGN_D, AT + "frame", D_ASSIGN_M, AT + "5", D_SUBTRACT_A_FROM_D, A_ASSIGN_D, D_ASSIGN_M, AT + "ret", M_ASSIGN_D]
        self.writeAsmLines(asmLines)

        self.writePop("argument", 0)

        asmLines = [AT + self.ramSymbol_dict["argument"], D_ASSIGN_M, AT + "1", D_ADD_A_TO_D, ATSP, M_ASSIGN_D]
        self.writeAsmLines(asmLines)

        asmLines = [AT + "frame", D_ASSIGN_M, AT + "1", D_SUBTRACT_A_FROM_D, A_ASSIGN_D, D_ASSIGN_M, AT + "THAT", M_ASSIGN_D]
        asmLines.extend([AT + "frame", D_ASSIGN_M, AT + "2", D_SUBTRACT_A_FROM_D, A_ASSIGN_D, D_ASSIGN_M, AT + "THIS", M_ASSIGN_D])
        asmLines.extend([AT + "frame", D_ASSIGN_M, AT + "3", D_SUBTRACT_A_FROM_D, A_ASSIGN_D, D_ASSIGN_M, AT + "ARG", M_ASSIGN_D])
        asmLines.extend([AT + "frame", D_ASSIGN_M, AT + "4", D_SUBTRACT_A_FROM_D, A_ASSIGN_D, D_ASSIGN_M, AT + "LCL", M_ASSIGN_D])
        self.writeAsmLines(asmLines)

        self.writeAsmLines([AT + "ret", A_ASSIGN_M, JMP])        

    def writeFalse(self):
        current_false = self.getCurrentFuncName(FALSE)
        current_func = ATFUNC + str(self.booleanCounter)
        asmLines = [
            current_false, ATSP, A_ASSIGN_M, M_SET_ZERO, ATSP, M_INCREMENT, current_func,
            JMP
        ]
        self.writeAsmLines(asmLines)

    def writeTrue(self):
        current_true = self.getCurrentFuncName(TRUE)
        current_func = ATFUNC + str(self.booleanCounter)
        asmLines = [
            current_true, ATSP, A_ASSIGN_M, M_SET_NEGATIVE_ONE, ATSP, M_INCREMENT, current_func,
            JMP
        ]
        self.writeAsmLines(asmLines)

    def writeFunc(self):
        self.writeAsmLines([self.getCurrentFuncName(FUNC)])

    def getCurrentFuncName(self, func_name):
        return func_name + str(self.booleanCounter) + ")"
    
    def setFileName(self, file_name):
        self.curFile = file_name

    def writeInit(self):
        asmLines = []        
        asmLines.append(AT + SPINDEX)
        asmLines.append(D_ASSIGN_A)
        asmLines.append(ATSP)
        asmLines.append(M_ASSIGN_D)
        self.writeAsmLines(asmLines)
        self.writeCall("Sys.init", "0")

    def close(self):
        asmLines = []
        asmLines.append("(END)")
        asmLines.append(AT + "END")
        asmLines.append(JMP)
        self.writeAsmLines(asmLines)

   