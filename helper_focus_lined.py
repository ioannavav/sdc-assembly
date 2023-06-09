import sys
import re
# import numpy as np

def argmax(x):
    return max(range(len(x)), key=lambda i: x[i])


def parse_file(registers):
    interesting_registers = []
    suspicious_registers = []
    
    # registers = line_of_file_path.split()[2:]  # Ignore the first two values
    # registers = registers.split()
    
    for register in registers:
        if register.startswith('{') and register.endswith('}'):  
            # Registers inside brackets are suspicious
            reg_list = register[1:-1].split(',')  # Remove the brackets and split by comma
            suspicious_registers.append(reg_list)
        else:  
            # Registers outside brackets are interesting
            interesting_registers.append(register)
    #print(interesting_registers)
    #print(suspicious_registers)
    return interesting_registers, suspicious_registers



def find_last_usage(file_path, register_names):
    last_usage = {register: None for register in register_names}
    
    with open(file_path, 'rb') as file:
        for line_num, line in enumerate(file, start=1):
            try:
                line = line.decode('utf-8').strip()
            except UnicodeDecodeError:
                continue  # Skip this line because it couldn't be decoded
            for register in register_names:
                # if re.search(r'\%' + register + '(?!x)', line):
                # print(f"searching: {register}")
                if re.search(rf'\b{register}\b', line):
                    last_usage[register] = (line_num, line)
                    
    return last_usage

def check_priorities(register_list, line_list, commands_list):
    priority_lists = [
        ['rax', 'eax', 'ax', 'al'],
        ['rcx', 'ecx', 'cx', 'cl'],
        ['rdx', 'edx', 'dx', 'dl'],
        ['rbx', 'ebx', 'bx', 'bl'],
        ['rsi', 'esi', 'si', 'sil'],
        ['rdi', 'edi', 'di', 'dil'],
        ['rsp', 'esp', 'sp', 'spl'],
        ['rbp', 'ebp', 'bp', 'bpl'],
        ['r8', 'r8d', 'r8w', 'r8b'],
        ['r9', 'r9d', 'r9w', 'r9b'],
        ['r10', 'r10d', 'r10w', 'r10b'],
        ['r11', 'r11d', 'r11w', 'r11b'],
        ['r12', 'r12d', 'r12w', 'r12b'],
        ['r13', 'r13d', 'r13w', 'r13b'],
        ['r14', 'r14d', 'r14w', 'r14b'],
        ['r15', 'r15d', 'r15w', 'r15b'],
        ['xmm0', 'ymm0', 'zmm0'],
        ['xmm1', 'ymm1', 'zmm1'],
        ['xmm2', 'ymm2', 'zmm2'],
        ['xmm3', 'ymm3', 'zmm3'],
        ['xmm4', 'ymm4', 'zmm4'],
        ['xmm5', 'ymm5', 'zmm5'],
        ['xmm6', 'ymm6', 'zmm6'],
        ['xmm7', 'ymm7', 'zmm7'],
        ['xmm8', 'ymm8', 'zmm8'],
        ['xmm9', 'ymm9', 'zmm9'],
        ['xmm10', 'ymm10', 'zmm10'],
        ['xmm11', 'ymm11', 'zmm11'],
        ['xmm12', 'ymm12', 'zmm12'],
        ['xmm13', 'ymm13', 'zmm13'],
        ['xmm14', 'ymm14', 'zmm14'],
        ['xmm15', 'ymm15', 'zmm15'],
        ['xmm16', 'ymm16', 'zmm16'],
        ['xmm17', 'ymm17', 'zmm17'],
        ['xmm18', 'ymm18', 'zmm18'],
        ['xmm19', 'ymm19', 'zmm19'],
        ['xmm20', 'ymm20', 'zmm20'],
        ['xmm21', 'ymm21', 'zmm21'],
        ['xmm22', 'ymm22', 'zmm22'],
        ['xmm23', 'ymm23', 'zmm23'],
        ['xmm24', 'ymm24', 'zmm24'],
        ['xmm25', 'ymm25', 'zmm25'],
        ['xmm26', 'ymm26', 'zmm26'],
        ['xmm27', 'ymm27', 'zmm27'],
        ['xmm28', 'ymm28', 'zmm28'],
        ['xmm29', 'ymm29', 'zmm29'],
        ['xmm30', 'ymm30', 'zmm30'],
        ['xmm31', 'ymm31', 'zmm31'],
    ]

    # Create a dictionary to store registers with their line numbers and commands
    reg_dict = {k: (v, commands_list[i]) for i, (k, v) in enumerate(zip(register_list, line_list))}

    new_register_list = []
    new_line_list = []
    new_commands_list = []

    # Iterate through priority_lists
    for sublist in priority_lists:
        max_line = -1
        max_reg = None
        max_command = None
        zero_line_regs = []
        zero_line_cmds = []
        # Check if a register from the sublist is in reg_dict and if its line number is larger
        for reg in sublist:
            if reg in reg_dict:
                if reg_dict[reg][0] > max_line:
                    max_line = reg_dict[reg][0]
                    max_reg = reg
                    max_command = reg_dict[reg][1]
                elif reg_dict[reg][0] == 0:
                    zero_line_regs.append(reg)
                    zero_line_cmds.append(reg_dict[reg][1])
        # If a register was found, add it to the new lists
        if max_reg is not None:
            new_register_list.append(max_reg)
            new_line_list.append(max_line)
            new_commands_list.append(max_command)
            # If max_line is 0, add all zero line registers and commands
            if max_line == 0:
                for i, reg in enumerate(zero_line_regs):
                    if reg != max_reg:
                        new_register_list.append(reg)
                        new_line_list.append(0)
                        new_commands_list.append(zero_line_cmds[i])
            # Remove all registers in the same group from the dictionary
            for reg in sublist:
                if reg in reg_dict:
                    del reg_dict[reg]

    # Add any remaining registers in reg_dict to the new lists
    for reg, values in reg_dict.items():
        new_register_list.append(reg)
        new_line_list.append(values[0])
        new_commands_list.append(values[1])

    return new_register_list, new_line_list, new_commands_list




if __name__ == '__main__':
    second_file_path = sys.argv[1]
    file_path = sys.argv[2:]
    print("                          <Y><M><D> <Time> --- <start address> -- <end address>")
    print(f"output_file: {second_file_path}")

    interesting_registers, suspicious_registers = parse_file(file_path)
    

    interesting_last_usage = find_last_usage(second_file_path, interesting_registers)
    suspicious_last_usage = [find_last_usage(second_file_path, item) for item in suspicious_registers]

    interesting_regs = []
    interesting_lines = []
    interesting_commands = []

    suspicious_regs = []
    suspicious_lines = []
    suspicious_commands = []

    overwriters_regs = []
    overwriters_lines = []
    overwriters_commands = []

    # Build the details for interesting and suspicious usages
    for register, usage in interesting_last_usage.items():
        interesting_regs.append(register)
        if usage is None:
            interesting_lines.append(0)
            interesting_commands.append(" - ")
        else:
            interesting_lines.append(usage[0])
            interesting_commands.append(usage[1])

    for item in suspicious_last_usage:
        temp_regs = []
        temp_lines = []
        temp_commands = []

        for register, usage in item.items():
            temp_regs.append(register)
            if usage is None:
                temp_lines.append(0)
                temp_commands.append(" - ")
            else:
                temp_lines.append(usage[0])
                temp_commands.append(usage[1])

        idx = argmax(temp_lines)
        suspicious_lines.append(temp_lines)
        suspicious_regs.append(temp_regs)
        suspicious_commands.append(temp_commands)
        overwriters_lines.append(temp_lines[idx])
        overwriters_regs.append(temp_regs[idx])
        overwriters_commands.append(temp_commands[idx])


    # Print the summary of interesting usages
    print("\n SUMMARY OF INTERESTING USAGES:")
    print(interesting_regs)
    print(interesting_lines)

    # Print the details of interesting usages
    print("\n DETAILS OF INTERESTING USAGES:")
    for i in range(len(interesting_regs)):
        if interesting_lines[i] == 0:
            print(f'{interesting_regs[i]} is not explicitly used within this block.')
        else:
            print(f'{interesting_regs[i]} was last used at line {interesting_lines[i]}:                      {interesting_commands[i]}')

    # Print the summary of suspicious usages
    print("\n SUMMARY OF SUSPICIOUS USAGES:")
    print(suspicious_regs)
    print(suspicious_lines)

    # Print the details of suspicious usages
    print("\n DETAILS OF SUSPICIOUS USAGES:")
    for i in range(len(suspicious_regs)):
        for j in range(len(suspicious_regs[i])):
            if suspicious_lines[i][j] == 0:
                print(f'{suspicious_regs[i][j]} is not explicitly used within this block.')
            else:
                print(f'{suspicious_regs[i][j]} was last used at line: {suspicious_lines[i][j]}:             {suspicious_commands[i][j]}')

    print("\n LAST INSTRUCTIONS TO USE REGISTERS OF INTEREST WITHIN THIS BLOCK:")
    final_regs, final_lines, final_commands = check_priorities(interesting_regs, interesting_lines, interesting_commands)

    for ind,i in enumerate(final_regs):
            print("Register:", i, "      line in output file:", final_lines[ind], "      command:", final_commands[ind])
            
    print("\n -------------------------------------end of block-----------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------\n")