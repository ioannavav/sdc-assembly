import re
import sys

# Define the sequence of commands we expect to remove at the end and at the beginning
end_sequence = [('push', '%rax'), ('push', '%rdi'), ('push', '%rsi'), ('push', '%rdx'), ('push', '%rcx'),
                ('push', '%r8'), ('push', '%r9'), ('push', '%r10'), ('push', '%r11'), ('call', 'print_registers')]
begin_sequence = [('pop', '%r11'), ('pop', '%r10'), ('pop', '%r9'), ('pop', '%r8'), ('pop', '%rcx'),
                  ('pop', '%rdx'), ('pop', '%rsi'), ('pop', '%rdi'), ('pop', '%rax')]

def parse_gdb_output(filename):
    buffer = []
    with open(filename, 'rb') as f:
        for binary_line in f:
            try:
                # Try to decode the line, ignoring lines we don't understand
                line = binary_line.decode('utf-8')
            except UnicodeDecodeError:
                continue

            # Skip lines that are breakpoints
            if "Breakpoint" in line:
                continue

            # Try to match assembly instruction lines
            match = re.match(r'(\d+)\s+(.*\s+.*\s+.*)|(.+\sat\s.+:.+)', line)
            if match:

                #ignore lines like main () at <file> that show us in which function we're in
                function_declaration = re.match(r'.+\(\)\sat\s.+:.+', line)
                if function_declaration:
                    continue

                buffer.append(line)

                # If buffer contains the expected end sequence, clear it
                if len(buffer) >= len(end_sequence):
                    for i, (expected_op, expected_arg) in enumerate(end_sequence):
                        if expected_op not in buffer[-len(end_sequence) + i] or expected_arg not in buffer[-len(end_sequence) + i]:
                            break
                    else:  # If we didn't break from the loop, all lines matched
                        buffer = buffer[:-len(end_sequence)]

                # If buffer contains the expected beginning sequence, remove it
                if len(buffer) >= len(begin_sequence):
                    for i, (expected_op, expected_arg) in enumerate(begin_sequence):
                        if expected_op not in buffer[i] or expected_arg not in buffer[i]:
                            break
                    else:  # If we didn't break from the loop, all lines matched
                        buffer = buffer[len(begin_sequence):]

        # Print any remaining lines
        for line in buffer:
            print(line, end='')





# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python3 last_step_parser.py <filename>")
    sys.exit(1)

# Get the input file name from command-line arguments
input_file = sys.argv[1]
parse_gdb_output(input_file)

