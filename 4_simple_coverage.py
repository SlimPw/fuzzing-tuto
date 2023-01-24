import random
from Coverage import Coverage

def fuzzer(max_length=100, char_start=32, char_range=32):

    length = random.randint(0, max_length + 1)
    out = ""
    for i in range(length):
        out += chr(random.randint(char_start, char_start+char_range))
    return out


def cgi_decode(s):
    """Decode the CGI-encoded string `s`:
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string.  Raise `ValueError` for invalid inputs."""

    # Mapping of hex digits to their integer values
    hex_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    }

    t = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == '+':
            t += ' '
        elif c == '%':
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values:
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t



coverage = set()
for i in range(1000):
    candidate = fuzzer(max_length=10)
    with Coverage() as cov:
        try:
            result = cgi_decode(candidate)
        except Exception as exc:
            pass

    new_coverage = frozenset(cov.coverage())
    if new_coverage.difference(coverage):
        print(candidate)

    coverage.update(new_coverage)

print(sorted([line for (method, line) in coverage if method == "cgi_decode"]))




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

valid_string = "foo=bar"


def coverage_fuzzer(seed, iterations, min_mutations=1, max_mutations=5):
    coverages_seen = set()
    population = seed
    valid = 0
    assert len(population) > 0

    for iteration in range(iterations):
        candidate = random.choice(population)
        trials = random.randint(min_mutations, max_mutations)
        for i in range(trials):
            candidate = mutate(candidate)

        with Coverage() as cov:
            try:
                result = cgi_decode(candidate)
            except Exception as exc:
                pass

        new_coverage = frozenset(cov.coverage())

        if new_coverage.difference(coverages_seen):
            # We have new coverage
            #print(new_coverage)
            population.append(candidate)
            coverages_seen.update(new_coverage)
            print(iteration, len(population))

    print(population)
    print(sorted([line for (method, line) in coverages_seen if method == "cgi_decode"]))


coverage_fuzzer([valid_string], 1000)

