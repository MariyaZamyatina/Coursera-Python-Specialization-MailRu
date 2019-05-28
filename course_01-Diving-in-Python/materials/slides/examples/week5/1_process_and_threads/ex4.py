# Файлы в родительском и дочернем процессе

# $ cat data.txt
# example string1
# example string2
# example string3

import os

f = open("data.txt")
foo = f.readline()

if os.fork() == 0:
    # дочерний процесс
    foo = f.readline()
    print("child:", foo)
else:
    # родительский процесс
    foo = f.readline()
    print("parent:", foo)
