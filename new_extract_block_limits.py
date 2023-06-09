import re
import sys
from collections import defaultdict

def process_text(input_text):
    # Split the text into blocks using regex
    blocks = re.split(r"(Block \d+:\n)", input_text)
    processed_blocks = defaultdict(str)

    for i in range(1, len(blocks), 2):
        block_name = blocks[i]
        block_content = blocks[i+1]
        
        # Merge the block contents
        processed_blocks[block_name] += block_content

    result = []
    for block_name, block_content in processed_blocks.items():
        # Remove specific duplicate lines
        block_content_lines = block_content.split('\n')
        clean_lines = []
        for line in block_content_lines:
            if "The return_address -next command after call- of Block" in line or "This block begins at the beginning of the program." in line:
                if line not in clean_lines:
                    clean_lines.append(line)
            else:
                clean_lines.append(line)
                
        block_content = '\n'.join(clean_lines)
        
        result.append(block_name)
        result.append(block_content)
    
    return "".join(result)


def extract_values(content):
    blocks = re.split("Block \d+:", content)[1:]
    ra_values = []
    prev_ra = "Beginning"

    for block in blocks:
        if 'interesting behavior' or 'Suspicious' in block:
            ra_current = re.search(r'The return_address -next command after call- of Block \d+ is: ([^\n]+)', block)
            ra_previous = re.search(r'The return_address of the previous block \d+ is: ([^\n]+)', block)
            
            interesting_behaviors = re.findall(r'(\w+) has interesting behavior', block)
            interesting_behaviors_str = ' '.join(interesting_behaviors)

            # Find all separate suspicious behaviors
            suspicious_behaviors = re.findall(r'Suspicious: {([^\}]+)}', block)
            suspicious_behaviors_str_list = ['{' + i + '}' for i in suspicious_behaviors]
            suspicious_behaviors_str_list = [x.replace(" ","") for x in suspicious_behaviors_str_list]

            ra_current_value = ra_current.group(1).strip() if ra_current else None
            ra_previous_value = ra_previous.group(1).strip() if ra_previous else prev_ra

            if ra_current_value:
                ra_values.append([ra_previous_value, ra_current_value, interesting_behaviors_str] + suspicious_behaviors_str_list)
                prev_ra = ra_current_value

    for index1, i in enumerate(ra_values):
        for index2, j in enumerate(i):
            if index2 < 2 and j != 'Beginning':
                j = j.replace(" ", "")
                bytes_list = [j[k:k+2] for k in range(0, len(j), 2)]
                bytes_list.reverse()
                hex_str = '0x' + ''.join(bytes_list)
                ra_values[index1][index2] = hex_str        

    return ('\n'.join(map(' '.join, ra_values)))



if len(sys.argv) != 2:
    print("Usage: python3 extract_block_limits.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as file:
    content = file.read()

processed_content = process_text(content)
print(extract_values(processed_content))

