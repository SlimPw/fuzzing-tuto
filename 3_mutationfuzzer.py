import random
from urllib.parse import urlparse

def fuzzer(max_length=100, char_start=32, char_range=32):

    length = random.randint(0, max_length + 1)
    out = ""
    for i in range(length):
        out += chr(random.randint(char_start, char_start+char_range))
    return out

def http_program(url):
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")

    # Do something with the URL
    return True

# Demonstrate how difficult it is
for i in range(1000):
    try:
        url = fuzzer()
        result = http_program(url)
        print("Success!")
    except ValueError:
        pass


valid_url = "http://studip.uni-passau.de/courses/software-analysis.html?foo=bar"

def insert_character(str):
    pos = random.randint(0, len(str))
    return str[:pos] + chr(random.randrange(32, 127)) + str[pos:]

def delete_character(str):
    if str == "":
        return str
    pos = random.randint(0, len(str) - 1)
    return str[:pos] + str[pos + 1:]

def replace_character(str):
    pos = random.randint(0, len(str) - 1)
    return str[:pos] + chr(random.randrange(32, 127)) + str[pos+1:]

def mutate(str):
    ops = [ insert_character, delete_character, replace_character ]
    op = random.choice(ops)
    return op(str)

count = 0
found = False
while not found:
    result = mutate(valid_url)
    if "https://" in result:
        found = True
    count += 1
print("Found after %d iterations: %s" % (count, result))


seed_input = "http://www.google.com/search?q=fuzzing"
mutations = 50
inp = seed_input
for i in range(mutations):
    if i % 5 == 0:
        print(i, "mutations:", repr(inp))
    inp = mutate(inp)
