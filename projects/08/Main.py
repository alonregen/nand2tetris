import sys
import os
import Parser
import CodeWriter

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

def process_vm_files(file_paths, outputFile):
    for file_path in file_paths:
        parseFile = Parser.Parser(file_path)
        currFileName = os.path.basename(file_path).split('.')[0]
        outputFile.setFileName(currFileName)
        while parseFile.hasMoreCommands():
            parseFile.advance()
            c_type = parseFile.commandType()
            if c_type == C_PUSH or c_type == C_POP:
                segment = parseFile.arg1()
                index = parseFile.arg2()
                # Push or pop command
                outputFile.writePushPop(c_type, segment, index)

            elif c_type == C_ARITHMETIC:
                command = parseFile.arg1()
                outputFile.writeArithmetic(command)  # Arithmetic command

            elif c_type == C_IF:
                dest = parseFile.arg1()
                outputFile.writeIf(dest)  # if command

            elif c_type == C_GOTO:
                dest = parseFile.arg1()
                outputFile.writeGOTO(dest)  # goto command

            elif c_type == C_LABEL:
                label = parseFile.arg1()
                outputFile.writeLabel(label)  # label command

            elif c_type == C_FUNCTION:
                name = parseFile.arg1()
                number = parseFile.arg2()
                outputFile.writeFuncation(name,number)
    
            elif c_type == C_CALL:
                name = parseFile.arg1()
                number = parseFile.arg2()
                outputFile.writeCall(name,number)  

            elif c_type == C_RETURN:
                outputFile.writeReturn()
    outputFile.close()


def process_directory(directory):
    vm_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.vm')]
    if vm_files:
        output_file = os.path.join(directory, os.path.basename(directory) + '.asm')
        outputFile = CodeWriter.CodeWriter(output_file)
        outputFile.writeInit()
        process_vm_files(vm_files, outputFile)


def process_single_file(file_path):
    output_file = file_path.rsplit('.', 1)[0] + '.asm'
    outputFile = CodeWriter.CodeWriter(output_file)
    process_vm_files([file_path], outputFile)


if __name__ == "__main__":
    #path = "/Users/alonregen/Desktop/code/nand2tetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm"
    #path = "/Users/alonregen/Desktop/code/nand2tetris/projects/08/FunctionCalls/StaticsTest"
    #path = "/Users/alonregen/Desktop/code/nand2tetris/projects/08/FunctionCalls/FibonacciElement"
    #path = "/Users/alonregen/Desktop/code/nand2tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm"
    #path = "/Users/alonregen/Desktop/code/nand2tetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm"
    path = sys.argv[1]


    if os.path.isdir(path):
        process_directory(path)
    elif os.path.isfile(path) and path.endswith('.vm'):
        process_single_file(path)
    else:
        print("Invalid path or file type. Please provide a directory or an .vm file.")
        sys.exit(1)
