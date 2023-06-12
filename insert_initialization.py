import sys

# Get the input and output file names from the command line arguments
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Usage: python3 insert_initialization.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Get the contents of the input file
with open(input_file, "r") as file:
    lines = file.readlines()

#inserted_count = 0
i = 0
#traversed_i = 0
#in_my_init = False
all_lines = [".global my_init\n",
"my_init:\n",
"\tvpxorq %zmm0, %zmm0, %zmm0\n",
"\tvpxorq %zmm1, %zmm1, %zmm1\n",
"\tvpxorq %zmm2, %zmm2, %zmm2\n",
"\tvpxorq %zmm3, %zmm3, %zmm3\n",
"\tvpxorq %zmm4, %zmm4, %zmm4\n",
"\tvpxorq %zmm5, %zmm5, %zmm5\n",
"\tvpxorq %zmm6, %zmm6, %zmm6\n",
"\tvpxorq %zmm7, %zmm7, %zmm7\n",
"\tvpxorq %zmm8, %zmm8, %zmm8\n",
"\tvpxorq %zmm9, %zmm9, %zmm9\n",
"\tvpxorq %zmm10, %zmm10, %zmm10\n",
"\tvpxorq %zmm11, %zmm11, %zmm11\n",
"\tvpxorq %zmm12, %zmm12, %zmm12\n",
"\tvpxorq %zmm13, %zmm13, %zmm13\n",
"\tvpxorq %zmm14, %zmm14, %zmm14\n",
"\tvpxorq %zmm15, %zmm15, %zmm15\n",
"\tvpxorq %zmm16, %zmm16, %zmm16\n",
"\tvpxorq %zmm17, %zmm17, %zmm17\n",
"\tvpxorq %zmm18, %zmm18, %zmm18\n",
"\tvpxorq %zmm19, %zmm19, %zmm19\n",
"\tvpxorq %zmm20, %zmm20, %zmm20\n",
"\tvpxorq %zmm21, %zmm21, %zmm21\n",
"\tvpxorq %zmm22, %zmm22, %zmm22\n",
"\tvpxorq %zmm23, %zmm23, %zmm23\n",
"\tvpxorq %zmm24, %zmm24, %zmm24\n",
"\tvpxorq %zmm25, %zmm25, %zmm25\n",
"\tvpxorq %zmm26, %zmm26, %zmm26\n",
"\tvpxorq %zmm27, %zmm27, %zmm27\n",
"\tvpxorq %zmm28, %zmm28, %zmm28\n",
"\tvpxorq %zmm29, %zmm29, %zmm29\n",
"\tvpxorq %zmm30, %zmm30, %zmm30\n",
"\tvpxorq %zmm31, %zmm31, %zmm31\n",
"\tretq\n",
"\n"]


while i < len(lines):
    all_lines.append(lines[i])
    if "main:" in lines[i]:
        all_lines.append("\tcallq my_init\n")
    i += 1

# Write the modified lines to the output file
with open(output_file, "w") as file:
    file.writelines(all_lines)

