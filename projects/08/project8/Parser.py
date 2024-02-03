import os

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"


command_dict = {
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    "push": "C_PUSH",
    "pop": "C_POP",
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if-goto": "C_IF",
    "function": "C_FUNCTION",
    "return": "C_RETURN",
    "call": "C_CALL",
    
}


class Parser:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.lines = [line.strip() for line in file if line.strip()
                          and not line.strip().startswith('//')]
        self.current_command_index = 0
        self.current_command = ""

    def hasMoreCommands(self):
        return self.current_command_index < len(self.lines)

    def advance(self):
        if self.hasMoreCommands():
            self.current_command = self.lines[self.current_command_index]
            self.current_command_index += 1

    def commandType(self):
        return command_dict[self.current_command.split()[0]]

    def arg1(self):
        command = self.current_command.split()[0]

        if command_dict[command] == C_RETURN:
            return None
        elif command_dict[command] == C_ARITHMETIC:
            return command
        else:
            return self.current_command.split()[1]

    def arg2(self):
        command = self.current_command.split()[0]
        if command_dict[command] == C_PUSH:
            return self.current_command.split()[2]
        elif command_dict[command] == C_POP:
            return self.current_command.split()[2]
        elif  command_dict[command] == C_FUNCTION:
            return self.current_command.split()[2]
        elif  command_dict[command] == C_CALL:
            return self.current_command.split()[2]
        else:
            return None
