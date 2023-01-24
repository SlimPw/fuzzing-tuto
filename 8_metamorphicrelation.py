
import random
import math

def get_random_test():
    return random.randint(0, 360)

x = get_random_test()
y = x + 2 * math.pi

result = math.sin(x)
print(x, result)
print(y, math.sin(y))

