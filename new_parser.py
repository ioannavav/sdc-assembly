import sys

# Check if the input file is provided as an argument
if len(sys.argv) < 2:
    print("Please provide the input file name as an argument.")
    sys.exit(1)

input_file = sys.argv[1]

# Open the input file
with open(input_file, 'r') as file:
    data = file.readlines()

# Variables to hold data
current_parser = None
block_counter = 0
block_total = 0
parsers = {}

# First pass to count blocks
for line in data:
    if 'Results for' in line:
        block_counter = 0
    elif line.startswith('return_address'):
        block_counter += 1
    block_total = max(block_total, block_counter)

# Reset variables for second pass
current_parser = None
block_counter = 0

# Second pass to process lines
inside_block = False
for line in data:
    # Identify parser
    if 'Results for' in line:
        current_parser = line.split('_')[1].strip().replace('.txt:', '')
        block_counter = 0
        if current_parser not in parsers:
            parsers[current_parser] = {}

    # Start of a block
    elif line.startswith('return_address'):
        inside_block = True
        if block_counter not in parsers[current_parser]:
            parsers[current_parser][block_counter] = []
        parsers[current_parser][block_counter].append(line)
        
    # Inside a block, store registers
    elif inside_block:
        parsers[current_parser][block_counter].append(line)

    # Block separator detected, increment block counter
    if line.startswith('-----') or line.startswith('_____'):
        inside_block = False
        block_counter += 1

# Generate output
for block in range(block_total):
    print(f"Block {block}:")
    for parser, blocks in parsers.items():
        print(f"***** {parser} *****")
        print(''.join(blocks[block]))
        print()
    print("---------------------------------")