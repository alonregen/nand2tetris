import sys
import os
import Parser
import CodeWriter

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"


def process_vm_files(file_paths, output_file):
    outputFile = CodeWriter.CodeWriter(output_file)
    for file_path in file_paths:
        parseFile = Parser.Parser(file_path)
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
    outputFile.close()


def process_directory(directory):
    vm_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.vm')]
    if vm_files:
        output_file = os.path.join(directory, os.path.basename(directory) + '.asm')
        process_vm_files(vm_files, output_file)


def process_single_file(file_path):
    output_file = file_path.rsplit('.', 1)[0] + '.asm'
    process_vm_files([file_path], output_file)


if __name__ == "__main__":
    path = sys.argv[1]

    if os.path.isdir(path):
        process_directory(path)
    elif os.path.isfile(path) and path.endswith('.vm'):
        process_single_file(path)
    else:
        print("Invalid path or file type. Please provide a directory or an .vm file.")
        sys.exit(1)
