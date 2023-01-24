import random

def fuzzer(max_length=100, char_start=32, char_range=32):
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

print(fuzzer())

print(fuzzer(1000, ord('a'), 26))
