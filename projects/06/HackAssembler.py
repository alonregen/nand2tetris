import sys

comp_dict = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

dest_dict = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}


jump_dict = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

predDefindedSymbol_dict = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}

label_dict ={}
instruction_lines = []


file_name = sys.argv[1]
output_file_name = "output.hack"



with open(file_name, 'r') as file:
    lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('//')]

    instruction_address = 0
    n=16
for line in lines:
    if line.startswith('(') and line.endswith(')'):  # Label
        label = line[1:-1]  # Extract label name
        label_dict[label] = instruction_address
    else:
        instruction_lines.append(line)
        instruction_address += 1

with open(output_file_name, 'w') as output_file:
    for line in instruction_lines:
        if line.startswith('@'):  # A-instruction
            symbol = line[1:]
            if symbol.isdigit(): 
                number = int(symbol)
            elif symbol in predDefindedSymbol_dict:
                number = predDefindedSymbol_dict.get(symbol)
            elif symbol in label_dict:
                number =label_dict.get(symbol)
            else:
                label_dict[symbol] = n
                number = n
                n=n+1 
            binary_number = format(number, '016b')
            output_file.write(binary_number + "\n")
        elif line: # C instruction 
            newline = "111"
            if ';' in line and not '=' in line:
                comp, jump = line.split(';')
                newline += comp_dict.get(comp)
                newline += "000"
                newline += jump_dict.get(jump)
            elif ';' in line and '=' in line:
                firstPart , secondPart= line.split('=')
                secondPart.split(';')
                newline += comp_dict.get(secondPart[0])
                newline += dest_dict.get(firstPart[0])
                newline += jump_dict.get(secondPart[1])
            elif '=' in line:
                firstPart = line.split('=')
                newline += comp_dict.get(firstPart[1])
                newline += dest_dict.get(firstPart[0])
                newline += "000"      
            output_file.write(newline + "\n")


