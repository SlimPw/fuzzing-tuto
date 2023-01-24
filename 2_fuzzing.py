import random

def fuzzer(max_length=100, char_start=32, char_range=32):

    length = random.randint(0, max_length + 1)
    out = ""
    for i in range(length):
        out += chr(random.randint(char_start, char_start+char_range))
    return out


import os
import tempfile

basename = "input.txt"
tempdir = tempfile.mkdtemp()
FILE = os.path.join(tempdir, basename)

import subprocess
program = "bc"

trials = 1000

runs = []
for i in range(trials):
    data = fuzzer()
    with open(FILE, "w") as f:
        f.write(data)
    result = subprocess.run([program, FILE],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    runs.append((data, result))

print(sum(1 for (data, result) in runs if result.stderr == ""))

print(sum(1 for (data, result) in runs if result.returncode != 0))
