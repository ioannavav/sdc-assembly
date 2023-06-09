# Call is as: echo "0x0000000000401155 0x0000000000401173" | gdb -batch -x gdb_script.py

import gdb
import re

def get_program_start():
    # Set a temporary breakpoint at main
    gdb.execute('tbreak main')
    gdb.execute('run')

    # Get the program counter
    start_addr = gdb.parse_and_eval('$pc')

    # Delete all breakpoints
    gdb.execute('delete')

    # Cast gdb.Value to int and return it
    return int(start_addr)

# Handle inputs to gdb_script.py
input_string = input()
split_string = input_string.split()
start_addr = split_string[0]
end_addr = split_string[1]
end_addr = int(end_addr, 16)
print("****", end_addr)
optional_arg = None
if len(split_string) > 2:
    optional_arg = split_string[2]


program_name = "./final_test"

gdb.execute("file " + program_name)


# If 'Beginning' is specified, get the start of the program
if start_addr.lower() == 'beginning':
    start_addr = get_program_start()
    print("@@@@", start_addr)
    gdb.execute("break *{}".format(hex(start_addr)))
else:
    start_addr = int(start_addr, 16)
    print("@@@@", start_addr)
    gdb.execute("break *{}".format(start_addr))

class StepUntil(gdb.Command):
    def __init__(self):
        super(StepUntil, self).__init__("step_until", gdb.COMMAND_USER)


    def invoke(self, arg, from_tty):
        while True:
            # Get the next instruction
            pc = gdb.selected_frame().pc()  
            if pc == end_addr:
                break
            inst = gdb.execute("x/i $pc", to_string=True)

            # Check if it's a call instruction
            if 'call' in inst:
                # Extract call target
                match = re.search(r'callq?\s*(0x[a-f0-9]+)\s*<(.+)>', inst)
                if match is not None:
                    target_name = match.group(2)

                    # Check if the function is in the PLT
                    if '@plt' in target_name:
                        print("Ommitting: ", target_name, "......")
                        gdb.execute("nexti")
                        continue
                    # Check if the function is print_registers
                    elif 'print_registers' in target_name:
                        print("Reached: ", target_name, "......")
                        break

            # If not a function call or not a PLT function, step into
            gdb.execute("stepi")

    

# Instantiate StepUntil class
StepUntil()

#gdb.execute("break *{}".format(start_addr))
if optional_arg is not None:
    gdb.execute("run " + optional_arg)
else:
    gdb.execute("run")
gdb.execute("step_until")
gdb.execute("quit")
