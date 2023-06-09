#!/bin/bash

# Check input parameters
TESTING_INPUTS=()
DEFAULT_INPUTS=()
INPUT_MODE="TESTING"

while (( "$#" )); do
  if [[ "$1" == "--" ]]; then
    INPUT_MODE="DEFAULT"
    shift
    continue
  fi

  if [[ $INPUT_MODE == "TESTING" ]]; then
    TESTING_INPUTS+=("$1")
  else
    DEFAULT_INPUTS+=("$1")
  fi

  shift
done

# Assign input parameters to variables
input_file=${TESTING_INPUTS[0]}
block_size=${TESTING_INPUTS[1]}
limit=${TESTING_INPUTS[2]}
cores=("${TESTING_INPUTS[@]:3}")  # Get the cores parameters as an array

# Get the base file name without extension
base_name=$(basename $input_file .c)

# Compile the C code to assembly
clang -S -o $base_name.s $input_file

# Insert the function calls into the assembly code
if [[ -z $limit ]]; then
    python3 insert_calls_with_push.py $base_name.s modified_$base_name.s $block_size
else
    python3 insert_calls_with_push.py $base_name.s modified_$base_name.s $block_size $limit
fi

# Link the modified assembly code with the print_registers assembly code
clang -g -o final_test modified_$base_name.s print_registers.s

# Array of register names
declare -a register_names=("return_address" "r15" "r14" "r13" "r12" "r11" "r10" "r9" "r8" "rbp" "rdi" "rsi" "rdx" "rcx" "rbx" "rax"
                           "zmm0_a" "zmm0_b" "zmm0_c" "zmm0_d" "zmm0_e" "zmm0_f" "zmm0_g" "zmm0_h"
                           "zmm1_a" "zmm1_b" "zmm1_c" "zmm1_d" "zmm1_e" "zmm1_f" "zmm1_g" "zmm1_h"
                           "zmm2_a" "zmm2_b" "zmm2_c" "zmm2_d" "zmm2_e" "zmm2_f" "zmm2_g" "zmm2_h"
                           "zmm3_a" "zmm3_b" "zmm3_c" "zmm3_d" "zmm3_e" "zmm3_f" "zmm3_g" "zmm3_h"
                           "zmm4_a" "zmm4_b" "zmm4_c" "zmm4_d" "zmm4_e" "zmm4_f" "zmm4_g" "zmm4_h"
                           "zmm5_a" "zmm5_b" "zmm5_c" "zmm5_d" "zmm5_e" "zmm5_f" "zmm5_g" "zmm5_h"
                           "zmm6_a" "zmm6_b" "zmm6_c" "zmm6_d" "zmm6_e" "zmm6_f" "zmm6_g" "zmm6_h"
                           "zmm7_a" "zmm7_b" "zmm7_c" "zmm7_d" "zmm7_e" "zmm7_f" "zmm7_g" "zmm7_h"
                           "zmm8_a" "zmm8_b" "zmm8_c" "zmm8_d" "zmm8_e" "zmm8_f" "zmm8_g" "zmm8_h"
                           "zmm9_a" "zmm9_b" "zmm9_c" "zmm9_d" "zmm9_e" "zmm9_f" "zmm9_g" "zmm9_h"
                           "zmm10_a" "zmm10_b" "zmm10_c" "zmm10_d" "zmm10_e" "zmm10_f" "zmm10_g" "zmm10_h"
                           "zmm11_a" "zmm11_b" "zmm11_c" "zmm11_d" "zmm11_e" "zmm11_f" "zmm11_g" "zmm11_h"
                           "zmm12_a" "zmm12_b" "zmm12_c" "zmm12_d" "zmm12_e" "zmm12_f" "zmm12_g" "zmm12_h"
                           "zmm13_a" "zmm13_b" "zmm13_c" "zmm13_d" "zmm13_e" "zmm13_f" "zmm13_g" "zmm13_h"
                           "zmm14_a" "zmm14_b" "zmm14_c" "zmm14_d" "zmm14_e" "zmm14_f" "zmm14_g" "zmm14_h"
                           "zmm15_a" "zmm15_b" "zmm15_c" "zmm15_d" "zmm15_e" "zmm15_f" "zmm15_g" "zmm15_h"
                           "zmm16_a" "zmm16_b" "zmm16_c" "zmm16_d" "zmm16_e" "zmm16_f" "zmm16_g" "zmm16_h"
                           "zmm17_a" "zmm17_b" "zmm17_c" "zmm17_d" "zmm17_e" "zmm17_f" "zmm17_g" "zmm17_h"
                           "zmm18_a" "zmm18_b" "zmm18_c" "zmm18_d" "zmm18_e" "zmm18_f" "zmm18_g" "zmm18_h"
                           "zmm19_a" "zmm19_b" "zmm19_c" "zmm19_d" "zmm19_e" "zmm19_f" "zmm19_g" "zmm19_h"
                           "zmm20_a" "zmm20_b" "zmm20_c" "zmm20_d" "zmm20_e" "zmm20_f" "zmm20_g" "zmm20_h"
                           "zmm21_a" "zmm21_b" "zmm21_c" "zmm21_d" "zmm21_e" "zmm21_f" "zmm21_g" "zmm21_h"
                           "zmm22_a" "zmm22_b" "zmm22_c" "zmm22_d" "zmm22_e" "zmm22_f" "zmm22_g" "zmm22_h"
                           "zmm23_a" "zmm23_b" "zmm23_c" "zmm23_d" "zmm23_e" "zmm23_f" "zmm23_g" "zmm23_h"
                           "zmm24_a" "zmm24_b" "zmm24_c" "zmm24_d" "zmm24_e" "zmm24_f" "zmm24_g" "zmm24_h"
                           "zmm25_a" "zmm25_b" "zmm25_c" "zmm25_d" "zmm25_e" "zmm25_f" "zmm25_g" "zmm25_h"
                           "zmm26_a" "zmm26_b" "zmm26_c" "zmm26_d" "zmm26_e" "zmm26_f" "zmm26_g" "zmm26_h"
                           "zmm27_a" "zmm27_b" "zmm27_c" "zmm27_d" "zmm27_e" "zmm27_f" "zmm27_g" "zmm27_h"
                           "zmm28_a" "zmm28_b" "zmm28_c" "zmm28_d" "zmm28_e" "zmm28_f" "zmm28_g" "zmm28_h"
                           "zmm29_a" "zmm29_b" "zmm29_c" "zmm29_d" "zmm29_e" "zmm29_f" "zmm29_g" "zmm29_h"
                           "zmm30_a" "zmm30_b" "zmm30_c" "zmm30_d" "zmm30_e" "zmm30_f" "zmm30_g" "zmm30_h"
                           "zmm31_a" "zmm31_b" "zmm31_c" "zmm31_d" "zmm31_e" "zmm31_f" "zmm31_g" "zmm31_h" )

# Array of general purpose register names
declare -a general_register_names=("r15" "r14" "r13" "r12" "r11" "r10" "r9" "r8")

# Array to hold unused registers
declare -a unused_register_names=()

# Check which general purpose registers are not used
for register in "${general_register_names[@]}"; do
    if ! grep -q "$register" "$base_name.s"; then
        echo "Register $register is not used."
        unused_register_names+=("$register")
    fi
done

# Execute the resulting program and capture its output
# If cores parameters are provided, use taskset to bind the program to the specified cores
declare -a results=()


if [[ ${#cores[@]} -eq 0 ]]; then
    ./final_test ${DEFAULT_INPUTS[@]} | xxd > my_binary_output.txt
    results+=("parser.txt")
else
    rm -f my_binary_output.txt  # Remove the old parser.txt file
    for core in "${cores[@]}"; do
        echo "Running on core $core"
        parser_file="core_$core.txt"
        if [[ ${#DEFAULT_INPUTS[@]} -ne 0 ]]; then
            taskset -c $core ./final_test ${DEFAULT_INPUTS[@]} | xxd > $parser_file
            #### taskset -c $core ./final_test $core | xxd > $parser_file
        else
            taskset -c $core ./final_test | xxd > $parser_file
        fi
        
        results+=($parser_file)
    done
fi

declare -i diff_flag=0
declare -i same_flag=0


# If only one core was used, just print the results normally
if [[ ${#cores[@]} -eq 1 ]]; then
    i=0
    while read -r line; do
        # Extract the two register values from the line
        register_value1=${line:10:20}
        register_value2=${line:30:20}

        # Only print register values if they are not in the unused_register_names array
        if [[ ! " ${unused_register_names[*]} " == *" ${register_names[$((i%272))]} "* ]]; then
           if [[ ! ${register_names[$((i%272))]} == "useless_alignment" ]]; then
            echo "${register_names[$((i%272))]}: $register_value1"
           fi
        fi
        i=$((i+1))
        if [[ ! " ${unused_register_names[*]} " == *" ${register_names[$((i%272))]} "* ]]; then
            if [[ "$register_value2" =~ [^[:space:]] ]]; then
                if [[ ! ${register_names[$((i%272))]} == "useless_alignment" ]]; then
                    echo "${register_names[$((i%272))]}: $register_value2"
                fi
            fi
        fi
        i=$((i+1))

        # Print a horizontal line before the next iteration of registers
        if (( i % 272 == 0 )); then
            echo "-----------------------------"
        fi
    done < ${results[0]}
else
    # Print the results for each core separately
    for parser_file in "${results[@]}"; do
        echo "Results for $parser_file:"
        i=0
        while read -r line; do
            register_value1=${line:10:20}
            register_value2=${line:30:20}

            if [[ ! " ${unused_register_names[*]} " == *" ${register_names[$((i%272))]} "* ]]; then
                if [[ ! ${register_names[$((i%272))]} == "useless_alignment" ]]; then
                    echo "${register_names[$((i%272))]}: $register_value1"
                fi
                
                if [[ ${register_names[$((i%272))]} == "zmm31_h" ]]; then
                echo "-----------------------------"
                fi
            fi
            i=$((i+1))

            if [[ ! " ${unused_register_names[*]} " == *" ${register_names[$((i%272))]} "* ]]; then
                if [[ "$register_value2" =~ [^[:space:]] ]]; then 
                    if [[ ! ${register_names[$((i%272))]} == "useless_alignment" ]]; then
                       echo "${register_names[$((i%272))]}: $register_value2"
                    fi
                    
                fi
                if [[ ${register_names[$((i%272))]} == "zmm31_h" ]]; then
                echo "-----------------------------"
                fi
            fi
            i=$((i+1))
            
        done < $parser_file
        echo "*********************************"
    done
fi

