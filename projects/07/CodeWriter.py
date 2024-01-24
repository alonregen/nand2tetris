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

# symbol
AT = "@"
SPINDEX = "256"
ATSP = "@SP"
TEMP = "13"


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
        asmLines = ["@SP", "M=M-1", "A=M", "D=M-D"]
        self.writeAsmLines(asmLines)

    def constructComparison(self, jumpCommand):
        labelTrue = f"TRUE{self.booleanCounter}"
        labelFalse = f"FALSE{self.booleanCounter}"
        labelEnd = f"END{self.booleanCounter}"
        return [
            f"@{labelTrue}", jumpCommand, 
            f"@{labelFalse}", "0;JMP", 
            f"({labelTrue})", "D=-1", 
            f"@{labelEnd}", "0;JMP", 
            f"({labelFalse})", "D=0", 
            f"({labelEnd})"
        ]

    def pushResultToStack(self, asmLines):
        asmLines.extend(["@SP", "A=M", "M=D", "@SP", "M=M+1"])
        self.writeAsmLines(asmLines)



    def writePushPop(self, c_type, segment, index):
        if c_type == "C_PUSH":
            self.writePush(segment, index)
        else:
            self.writePop(segment, index)

    def writePop(self, segment, index):
        asmLines = ["@SP", "M=M-1", "A=M", "D=M"]
        if segment in ["temp", "pointer"]:
            address = str(int(self.ramSymbol_dict[segment]) + int(index))
            asmLines.extend(["@" + address, "M=D"])
        elif segment == "static":
            static_address = self.baseFilename + "." + str(index)
            asmLines.extend(["@" + static_address, "M=D"])
        else:  # local, argument, this, that
            asmLines.extend([
                "@" + str(self.ramSymbol_dict[segment]), "D=M",
                "@" + str(index), "D=D+A",
                "@R13", "M=D",  # Use R13 as a temporary variable
                "@SP", "A=M", "D=M",
                "@R13", "A=M", "M=D"
            ])
        self.writeAsmLines(asmLines)

    def writePush(self, segment, index):
        asmLines = []
        if segment == "constant":
            asmLines.extend(["@" + str(index), "D=A"])
        elif segment in ["temp", "pointer"]:
            address = str(int(self.ramSymbol_dict[segment]) + int(index))
            asmLines.extend(["@" + address, "D=M"])
        elif segment == "static":
            static_address = self.baseFilename + "." + str(index)
            asmLines.extend(["@" + static_address, "D=M"])
        else:  # local, argument, this, that
            asmLines.extend([
                "@" + str(self.ramSymbol_dict[segment]), "D=M",
                "@" + str(index), "D=D+A",
                "A=D", "D=M"
            ])
        asmLines.extend(["@SP", "A=M", "M=D", "@SP", "M=M+1"])
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


    def close(self):
        asmLines = []
        asmLines.append("(END)")
        asmLines.append(AT + "END")
        asmLines.append(JMP)
        self.writeAsmLines(asmLines)
    
