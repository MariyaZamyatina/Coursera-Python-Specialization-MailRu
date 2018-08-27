import sys

digit_string = sys.argv[1]

digit_sum = 0
for digit in digit_string:
    digit_sum += int(digit)

print(digit_sum)