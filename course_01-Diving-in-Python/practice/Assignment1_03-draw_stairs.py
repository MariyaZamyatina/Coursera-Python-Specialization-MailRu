import sys

num_steps = int(sys.argv[1])

for num_signs in range(1, num_steps+1):
    num_spaces = num_steps - num_signs
    print(" "*num_spaces + "#"*num_signs)