import sys

# Get the input and output file names from the command line arguments
if len(sys.argv) < 4 or len(sys.argv) > 5:
    print("Usage: python3 insert_calls.py input_file output_file frequency [limit]")
    sys.exit(1)
input_file = sys.argv[1]
output_file = sys.argv[2]
frequency = int(sys.argv[3])
limit = int(sys.argv[4]) if len(sys.argv) == 5 else None

# Get the contents of the input file
with open(input_file, "r") as file:
    lines = file.readlines()

# Insert the new line into the list of lines
new_lines = """\tpush %rax
\tpush %rdi
\tpush %rsi
\tpush %rdx
\tpush %rcx
\tpush %r8
\tpush %r9
\tpush %r10
\tpush %r11
\tcall print_registers
\tpop %r11
\tpop %r10
\tpop %r9
\tpop %r8
\tpop %rcx
\tpop %rdx
\tpop %rsi
\tpop %rdi
\tpop %rax
"""

inserted_count = 0
i = 0
traversed_i = 0
while i < len(lines):
    line = lines[i].lstrip()  # Remove leading white spaces and tabs
    if not line.startswith(".") and not line.startswith("#"):
        if (traversed_i + 1) % frequency == 0:
            if limit is not None and inserted_count >= limit:
                break
            lines.insert(i+(inserted_count), new_lines)
            inserted_count += 1
        traversed_i +=1
    i += 1

# Write the modified lines to the output file
with open(output_file, "w") as file:
    file.writelines(lines)

