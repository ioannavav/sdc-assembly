def process_file(filename):
    with open(filename, 'r') as f:
        block = None
        register_values = {}
        zmm_register_values = {}
        for line in f:
            line = line.strip()
            if 'Block' in line:
                if block is not None:
                    compare_values(register_values, block)
                    zmm_compare_values(zmm_register_values, block)
                block = line.split()[-1][:-1]
                register_values[block] = {}
                zmm_register_values[block] = {}
            elif '*****' in line:
                continue
            elif '--------------------' in line or len(line.strip()) == 0:
                continue
            elif line:
                if line.startswith('return_address'):
                    register, value = line.split(': ')
                    if register not in register_values[block]:
                        register_values[block][register] = []
                    register_values[block][register].append(value)
                    # put the return_address in the zmm blocks as well, because it's gonna be needed to determine the boundaries
                    zmm_register, zmm_value = line.split(': ')
                    if zmm_register not in zmm_register_values[block]:
                        zmm_register_values[block][zmm_register] = []
                    zmm_register_values[block][zmm_register].append(zmm_value)

                elif not line.startswith('zmm'):
                    register, value = line.split(': ')
                    if register not in register_values[block]:
                        register_values[block][register] = []
                    register_values[block][register].append(value)
                else:
                    zmm_register, zmm_value = line.split(': ')
                    if zmm_register not in zmm_register_values[block]:
                        zmm_register_values[block][zmm_register] = []
                    zmm_register_values[block][zmm_register].append(zmm_value)


        compare_values(register_values, block)
        zmm_compare_values(zmm_register_values, block)
"""
def process_file(filename):
    with open(filename, 'r') as f:
        block = None
        register_values = {}
        current_zmm_register = None
        current_zmm_values = []
        for line in f:
            line = line.strip()
            if 'Block' in line:
                if block is not None:
                    if current_zmm_register is not None:
                        register_values[block][current_zmm_register] = current_zmm_values
                        current_zmm_register = None
                        current_zmm_values = []
                    compare_values(register_values, block)
                block = line.split()[-1][:-1]
                register_values[block] = {}
            elif '*****' in line:
                continue
            elif '--------------------' in line or len(line.strip()) == 0:
                continue
            elif line:
                register, value = line.split(': ')
                if register.startswith('zmm'):
                    if register[4] != '_':
                        if current_zmm_register is not None:
                            register_values[block][current_zmm_register] = current_zmm_values
                            current_zmm_values = []
                        current_zmm_register = register
                    current_zmm_values.append(value)
                else:
                    if current_zmm_register is not None:
                        register_values[block][current_zmm_register] = current_zmm_values
                        current_zmm_register = None
                        current_zmm_values = []
                    if register not in register_values[block]:
                        register_values[block][register] = []
                    register_values[block][register].append(value)

        if current_zmm_register is not None:
            register_values[block][current_zmm_register] = current_zmm_values
        compare_values(register_values, block)
"""

def register_mapping(register):
    mappings = {
        'rax': ['eax', 'ax', 'al'],
        'rcx': ['ecx', 'cx', 'cl'],
        'rdx': ['edx', 'dx', 'dl'],
        'rbx': ['ebx', 'bx', 'bl'],
        'rsi': ['esi', 'si', 'sil'],
        'rdi': ['edi', 'di', 'dil'],
        'rsp': ['esp', 'sp', 'spl'],
        'rbp': ['ebp', 'bp', 'bpl'],
        'r8': ['r8d', 'r8w', 'r8b'],
        'r9': ['r9d', 'r9w', 'r9b'],
        'r10': ['r10d', 'r10w', 'r10b'],
        'r11': ['r11d', 'r11w', 'r11b'],
        'r12': ['r12d', 'r12w', 'r12b'],
        'r13': ['r13d', 'r13w', 'r13b'],
        'r14': ['r14d', 'r14w', 'r14b'],
        'r15': ['r15d', 'r15w', 'r15b'],
    }

    if register in mappings:
        return mappings[register][0], mappings[register][1], mappings[register][2]
    else:
        print(f'Invalid register: {register}')
        return None, None, None


def zmm_register_mapping(zmm_register):
    zmm_mappings = {
        'zmm0_a': ['xmm0', 'ymm0', 'zmm0'],
        'zmm0_b': ['xmm0', 'ymm0', 'zmm0'],
        'zmm0_c': ['ymm0', 'zmm0'],
        'zmm0_d': ['ymm0', 'zmm0'],
        'zmm0_e': ['zmm0'],
        'zmm0_f': ['zmm0'],
        'zmm0_g': ['zmm0'],
        'zmm0_h': ['zmm0'],
        'zmm1_a': ['xmm1', 'ymm1', 'zmm1'],
        'zmm1_b': ['xmm1', 'ymm1', 'zmm1'],
        'zmm1_c': ['ymm1', 'zmm1'],
        'zmm1_d': ['ymm1', 'zmm1'],
        'zmm1_e': ['zmm1'],
        'zmm1_f': ['zmm1'],
        'zmm1_g': ['zmm1'],
        'zmm1_h': ['zmm1'],
        'zmm2_a': ['xmm2', 'ymm2', 'zmm2'],
        'zmm2_b': ['xmm2', 'ymm2', 'zmm2'],
        'zmm2_c': ['ymm2', 'zmm2'],
        'zmm2_d': ['ymm2', 'zmm2'],
        'zmm2_e': ['zmm2'],
        'zmm2_f': ['zmm2'],
        'zmm2_g': ['zmm2'],
        'zmm2_h': ['zmm2'],
        'zmm3_a': ['xmm3', 'ymm3', 'zmm3'],
        'zmm3_b': ['xmm3', 'ymm3', 'zmm3'],
        'zmm3_c': ['ymm3', 'zmm3'],
        'zmm3_d': ['ymm3', 'zmm3'],
        'zmm3_e': ['zmm3'],
        'zmm3_f': ['zmm3'],
        'zmm3_g': ['zmm3'],
        'zmm3_h': ['zmm3'],
        'zmm4_a': ['xmm4', 'ymm4', 'zmm4'],
        'zmm4_b': ['xmm4', 'ymm4', 'zmm4'],
        'zmm4_c': ['ymm4', 'zmm4'],
        'zmm4_d': ['ymm4', 'zmm4'],
        'zmm4_e': ['zmm4'],
        'zmm4_f': ['zmm4'],
        'zmm4_g': ['zmm4'],
        'zmm4_h': ['zmm4'],
        'zmm5_a': ['xmm5', 'ymm5', 'zmm5'],
        'zmm5_b': ['xmm5', 'ymm5', 'zmm5'],
        'zmm5_c': ['ymm5', 'zmm5'],
        'zmm5_d': ['ymm5', 'zmm5'],
        'zmm5_e': ['zmm5'],
        'zmm5_f': ['zmm5'],
        'zmm5_g': ['zmm5'],
        'zmm5_h': ['zmm5'],
        'zmm6_a': ['xmm6', 'ymm6', 'zmm6'],
        'zmm6_b': ['xmm6', 'ymm6', 'zmm6'],
        'zmm6_c': ['ymm6', 'zmm6'],
        'zmm6_d': ['ymm6', 'zmm6'],
        'zmm6_e': ['zmm6'],
        'zmm6_f': ['zmm6'],
        'zmm6_g': ['zmm6'],
        'zmm6_h': ['zmm6'],
        'zmm7_a': ['xmm7', 'ymm7', 'zmm7'],
        'zmm7_b': ['xmm7', 'ymm7', 'zmm7'],
        'zmm7_c': ['ymm7', 'zmm7'],
        'zmm7_d': ['ymm7', 'zmm7'],
        'zmm7_e': ['zmm7'],
        'zmm7_f': ['zmm7'],
        'zmm7_g': ['zmm7'],
        'zmm7_h': ['zmm7'],
        'zmm8_a': ['xmm8', 'ymm8', 'zmm8'],
        'zmm8_b': ['xmm8', 'ymm8', 'zmm8'],
        'zmm8_c': ['ymm8', 'zmm8'],
        'zmm8_d': ['ymm8', 'zmm8'],
        'zmm8_e': ['zmm8'],
        'zmm8_f': ['zmm8'],
        'zmm8_g': ['zmm8'],
        'zmm8_h': ['zmm8'],
        'zmm9_a': ['xmm9', 'ymm9', 'zmm9'],
        'zmm9_b': ['xmm9', 'ymm9', 'zmm9'],
        'zmm9_c': ['ymm9', 'zmm9'],
        'zmm9_d': ['ymm9', 'zmm9'],
        'zmm9_e': ['zmm9'],
        'zmm9_f': ['zmm9'],
        'zmm9_g': ['zmm9'],
        'zmm9_h': ['zmm9'],
        'zmm10_a': ['xmm10', 'ymm10', 'zmm10'],
        'zmm10_b': ['xmm10', 'ymm10', 'zmm10'],
        'zmm10_c': ['ymm10', 'zmm10'],
        'zmm10_d': ['ymm10', 'zmm10'],
        'zmm10_e': ['zmm10'],
        'zmm10_f': ['zmm10'],
        'zmm10_g': ['zmm10'],
        'zmm10_h': ['zmm10'],
        'zmm11_a': ['xmm11', 'ymm11', 'zmm11'],
        'zmm11_b': ['xmm11', 'ymm11', 'zmm11'],
        'zmm11_c': ['ymm11', 'zmm11'],
        'zmm11_d': ['ymm11', 'zmm11'],
        'zmm11_e': ['zmm11'],
        'zmm11_f': ['zmm11'],
        'zmm11_g': ['zmm11'],
        'zmm11_h': ['zmm11'],
        'zmm12_a': ['xmm12', 'ymm12', 'zmm12'],
        'zmm12_b': ['xmm12', 'ymm12', 'zmm12'],
        'zmm12_c': ['ymm12', 'zmm12'],
        'zmm12_d': ['ymm12', 'zmm12'],
        'zmm12_e': ['zmm12'],
        'zmm12_f': ['zmm12'],
        'zmm12_g': ['zmm12'],
        'zmm12_h': ['zmm12'],
        'zmm13_a': ['xmm13', 'ymm13', 'zmm13'],
        'zmm13_b': ['xmm13', 'ymm13', 'zmm13'],
        'zmm13_c': ['ymm13', 'zmm13'],
        'zmm13_d': ['ymm13', 'zmm13'],
        'zmm13_e': ['zmm13'],
        'zmm13_f': ['zmm13'],
        'zmm13_g': ['zmm13'],
        'zmm13_h': ['zmm13'],
        'zmm14_a': ['xmm14', 'ymm14', 'zmm14'],
        'zmm14_b': ['xmm14', 'ymm14', 'zmm14'],
        'zmm14_c': ['ymm14', 'zmm14'],
        'zmm14_d': ['ymm14', 'zmm14'],
        'zmm14_e': ['zmm14'],
        'zmm14_f': ['zmm14'],
        'zmm14_g': ['zmm14'],
        'zmm14_h': ['zmm14'],
        'zmm15_a': ['xmm15', 'ymm15', 'zmm15'],
        'zmm15_b': ['xmm15', 'ymm15', 'zmm15'],
        'zmm15_c': ['ymm15', 'zmm15'],
        'zmm15_d': ['ymm15', 'zmm15'],
        'zmm15_e': ['zmm15'],
        'zmm15_f': ['zmm15'],
        'zmm15_g': ['zmm15'],
        'zmm15_h': ['zmm15'],
        'zmm16_a': ['xmm16', 'ymm16', 'zmm16'],
        'zmm16_b': ['xmm16', 'ymm16', 'zmm16'],
        'zmm16_c': ['ymm16', 'zmm16'],
        'zmm16_d': ['ymm16', 'zmm16'],
        'zmm16_e': ['zmm16'],
        'zmm16_f': ['zmm16'],
        'zmm16_g': ['zmm16'],
        'zmm16_h': ['zmm16'],
        'zmm17_a': ['xmm17', 'ymm17', 'zmm17'],
        'zmm17_b': ['xmm17', 'ymm17', 'zmm17'],
        'zmm17_c': ['ymm17', 'zmm17'],
        'zmm17_d': ['ymm17', 'zmm17'],
        'zmm17_e': ['zmm17'],
        'zmm17_f': ['zmm17'],
        'zmm17_g': ['zmm17'],
        'zmm17_h': ['zmm17'],
        'zmm18_a': ['xmm18', 'ymm18', 'zmm18'],
        'zmm18_b': ['xmm18', 'ymm18', 'zmm18'],
        'zmm18_c': ['ymm18', 'zmm18'],
        'zmm18_d': ['ymm18', 'zmm18'],
        'zmm18_e': ['zmm18'],
        'zmm18_f': ['zmm18'],
        'zmm18_g': ['zmm18'],
        'zmm18_h': ['zmm18'],
        'zmm19_a': ['xmm19', 'ymm19', 'zmm19'],
        'zmm19_b': ['xmm19', 'ymm19', 'zmm19'],
        'zmm19_c': ['ymm19', 'zmm19'],
        'zmm19_d': ['ymm19', 'zmm19'],
        'zmm19_e': ['zmm19'],
        'zmm19_f': ['zmm19'],
        'zmm19_g': ['zmm19'],
        'zmm19_h': ['zmm19'],
        'zmm20_a': ['xmm20', 'ymm20', 'zmm20'],
        'zmm20_b': ['xmm20', 'ymm20', 'zmm20'],
        'zmm20_c': ['ymm20', 'zmm20'],
        'zmm20_d': ['ymm20', 'zmm20'],
        'zmm20_e': ['zmm20'],
        'zmm20_f': ['zmm20'],
        'zmm20_g': ['zmm20'],
        'zmm20_h': ['zmm20'],
        'zmm21_a': ['xmm21', 'ymm21', 'zmm21'],
        'zmm21_b': ['xmm21', 'ymm21', 'zmm21'],
        'zmm21_c': ['ymm21', 'zmm21'],
        'zmm21_d': ['ymm21', 'zmm21'],
        'zmm21_e': ['zmm21'],
        'zmm21_f': ['zmm21'],
        'zmm21_g': ['zmm21'],
        'zmm21_h': ['zmm21'],
        'zmm22_a': ['xmm22', 'ymm22', 'zmm22'],
        'zmm22_b': ['xmm22', 'ymm22', 'zmm22'],
        'zmm22_c': ['ymm22', 'zmm22'],
        'zmm22_d': ['ymm22', 'zmm22'],
        'zmm22_e': ['zmm22'],
        'zmm22_f': ['zmm22'],
        'zmm22_g': ['zmm22'],
        'zmm22_h': ['zmm22'],
        'zmm23_a': ['xmm23', 'ymm23', 'zmm23'],
        'zmm23_b': ['xmm23', 'ymm23', 'zmm23'],
        'zmm23_c': ['ymm23', 'zmm23'],
        'zmm23_d': ['ymm23', 'zmm23'],
        'zmm23_e': ['zmm23'],
        'zmm23_f': ['zmm23'],
        'zmm23_g': ['zmm23'],
        'zmm23_h': ['zmm23'],
        'zmm24_a': ['xmm24', 'ymm24', 'zmm24'],
        'zmm24_b': ['xmm24', 'ymm24', 'zmm24'],
        'zmm24_c': ['ymm24', 'zmm24'],
        'zmm24_d': ['ymm24', 'zmm24'],
        'zmm24_e': ['zmm24'],
        'zmm24_f': ['zmm24'],
        'zmm24_g': ['zmm24'],
        'zmm24_h': ['zmm24'],
        'zmm25_a': ['xmm25', 'ymm25', 'zmm25'],
        'zmm25_b': ['xmm25', 'ymm25', 'zmm25'],
        'zmm25_c': ['ymm25', 'zmm25'],
        'zmm25_d': ['ymm25', 'zmm25'],
        'zmm25_e': ['zmm25'],
        'zmm25_f': ['zmm25'],
        'zmm25_g': ['zmm25'],
        'zmm25_h': ['zmm25'],
        'zmm26_a': ['xmm26', 'ymm26', 'zmm26'],
        'zmm26_b': ['xmm26', 'ymm26', 'zmm26'],
        'zmm26_c': ['ymm26', 'zmm26'],
        'zmm26_d': ['ymm26', 'zmm26'],
        'zmm26_e': ['zmm26'],
        'zmm26_f': ['zmm26'],
        'zmm26_g': ['zmm26'],
        'zmm26_h': ['zmm26'],
        'zmm27_a': ['xmm27', 'ymm27', 'zmm27'],
        'zmm27_b': ['xmm27', 'ymm27', 'zmm27'],
        'zmm27_c': ['ymm27', 'zmm27'],
        'zmm27_d': ['ymm27', 'zmm27'],
        'zmm27_e': ['zmm27'],
        'zmm27_f': ['zmm27'],
        'zmm27_g': ['zmm27'],
        'zmm27_h': ['zmm27'],
        'zmm28_a': ['xmm28', 'ymm28', 'zmm28'],
        'zmm28_b': ['xmm28', 'ymm28', 'zmm28'],
        'zmm28_c': ['ymm28', 'zmm28'],
        'zmm28_d': ['ymm28', 'zmm28'],
        'zmm28_e': ['zmm28'],
        'zmm28_f': ['zmm28'],
        'zmm28_g': ['zmm28'],
        'zmm28_h': ['zmm28'],
        'zmm29_a': ['xmm29', 'ymm29', 'zmm29'],
        'zmm29_b': ['xmm29', 'ymm29', 'zmm29'],
        'zmm29_c': ['ymm29', 'zmm29'],
        'zmm29_d': ['ymm29', 'zmm29'],
        'zmm29_e': ['zmm29'],
        'zmm29_f': ['zmm29'],
        'zmm29_g': ['zmm29'],
        'zmm29_h': ['zmm29'],
        'zmm30_a': ['xmm30', 'ymm30', 'zmm30'],
        'zmm30_b': ['xmm30', 'ymm30', 'zmm30'],
        'zmm30_c': ['ymm30', 'zmm30'],
        'zmm30_d': ['ymm30', 'zmm30'],
        'zmm30_e': ['zmm30'],
        'zmm30_f': ['zmm30'],
        'zmm30_g': ['zmm30'],
        'zmm30_h': ['zmm30'],
        'zmm31_a': ['xmm31', 'ymm31', 'zmm31'],
        'zmm31_b': ['xmm31', 'ymm31', 'zmm31'],
        'zmm31_c': ['ymm31', 'zmm31'],
        'zmm31_d': ['ymm31', 'zmm31'],
        'zmm31_e': ['zmm31'],
        'zmm31_f': ['zmm31'],
        'zmm31_g': ['zmm31'],
        'zmm31_h': ['zmm31'],
    }

    if zmm_register in zmm_mappings:
        return zmm_mappings[zmm_register]
    else:
        print(f'Invalid ZMM register: {zmm_register}')
        return None




def check_suspicion(lst, register, return_suspicion=False):
    reg_32, reg_16, reg_8 = register_mapping(register)

    first_32 = [x.replace(' ', '')[:8] for x in lst]
    suspicion_messages = []

    if len(set(first_32)) != 1 and len(set(first_32)) != len(first_32):
        suspicion_messages.append(reg_32)

    if len(set(first_32)) == len(first_32):
        first_16 = [x[:4] for x in first_32]
        if len(set(first_16)) != 1 and len(set(first_16)) != len(first_16):
            suspicion_messages.append(reg_16)

    first_8 = [x[:2] for x in first_32]
    if len(set(first_8)) != 1 and len(set(first_8)) != len(first_8):
        suspicion_messages.append(reg_8)

    if return_suspicion:
        return ['Suspicious: {' + ', '.join(suspicion_messages) + '}'] if suspicion_messages else []
    else:
        for msg in ['Suspicious: {' + ', '.join(suspicion_messages) + '}'] if suspicion_messages else []:
            print(msg)


def check_subsets(lst, register):
    reg_32, reg_16, reg_8 = register_mapping(register)

    first_32 = [x.replace(' ', '')[:8] for x in lst]
    first_16 = [x[:4] for x in first_32]
    first_8 = [x[:2] for x in first_32]

    if len(set(first_32)) != 1 and len(set(first_32)) != len(first_32):
        print(f'{reg_32} has interesting behavior!!!!!!!!!!')
        print(first_32)

    if len(set(first_16)) != 1 and len(set(first_16)) != len(first_16):
        print(f'{reg_16} has interesting behavior!!!!!!!!!!')
        print(first_16)
    
    if len(set(first_8)) != 1 and len(set(first_8)) != len(first_8):
        print(f'{reg_8} has interesting behavior!!!!!!!!!!')
        print(first_8)
    
        

def zmm_compare_values(zmm_register_values, block):
    zmm_interesting_registers = []

    for zmm_register, values in zmm_register_values[block].items():
        if len(set(values)) == 1:
            continue
        else: 
            # general purpose registers do not hold addresses, so even if they change across all cores it's interesting to us     
            zmm_interesting_registers.append((zmm_register, values))

    if zmm_interesting_registers:
        print(f'Block {block}:')
        for zmm_register, values in zmm_interesting_registers:
            all_interesting_zmm_registers = zmm_register_mapping(zmm_register)
            for zmm_i in all_interesting_zmm_registers:
                print(f'{zmm_i} has interesting behavior +++++++++++')
                print(values)
        print("The return_address -next command after call- of Block", block, "is:", zmm_register_values[block]['return_address'][0])
        if int(block) > 0:
            print("The return_address of the previous block", int(block)-1, "is:", zmm_register_values[str(int(block)-1)]['return_address'][0])
        else:
            print("This block begins at the beginning of the program.")
        print("------------------------------------------------------------------")




def compare_values(register_values, block):
    suspicion_messages = []
    interesting_registers = []

    for register, values in register_values[block].items():
        if len(set(values)) == 1:
            continue
        elif len(set(values)) == len(values):
            # here is when the register changes across all cores
            suspicion_messages.extend(check_suspicion(values, register, return_suspicion=True))
        else:      
            interesting_registers.append((register, values))

    if interesting_registers or suspicion_messages:
        print(f'Block {block}:')
        for register, values in interesting_registers:
            print(f'{register} has interesting behavior!!!!!!!!!!')
            print(values)
            check_subsets(values, register)
            
        for msg in suspicion_messages:
            print(msg)
        print("The return_address -next command after call- of Block", block, "is:", register_values[block]['return_address'][0])
        if int(block) > 0:
            print("The return_address of the previous block", int(block)-1, "is:", register_values[str(int(block)-1)]['return_address'][0])
        else:
            print("This block begins at the beginning of the program.")
        print("------------------------------------------------------------------")

    


import sys

if len(sys.argv) != 2:
    print("Usage: python3 your_script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
process_file(filename)
