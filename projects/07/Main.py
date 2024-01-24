import sys
import os
import Parser
import CodeWriter

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"


def process_vm_file(file_path):
    new_file_name = file_path.rsplit('.', 1)[0] + '.asm'
    parseFile = Parser.Parser(file_path)
    outputFile = CodeWriter.CodeWriter(new_file_name)
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
    for file_name in os.listdir(directory):
        if file_name.endswith('.vm'):
            file_path = os.path.join(directory, file_name)
            process_vm_file(file_path)


if __name__ == "__main__":
    path = sys.argv[1]

    if os.path.isdir(path):
        process_directory(path)
    elif os.path.isfile(path) and path.endswith('.vm'):
        process_vm_file(path)
    else:
        print("Invalid path or file type. Please provide a directory or an .vm file.")
        sys.exit(1)
