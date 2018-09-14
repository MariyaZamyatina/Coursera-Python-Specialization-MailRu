import sys

digit_string = sys.argv[1]

digit_sum = sum([int(digit) for digit in digit_string])

print(digit_sum)