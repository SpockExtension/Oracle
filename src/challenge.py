import random
import string
import time

def generate_random_strings(num_strings):
    random_strings = []
    for i in range(num_strings):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        random_strings.append(random_string)
    return random_strings

def write_to_file(filename, strings):
    with open(filename, 'w') as f:
        for s in strings:
            f.write(s + '\n')

while True:
    # Generate 20 random strings
    random_strings = generate_random_strings(20)

    # Write the strings to a file
    write_to_file('nonce.txt', random_strings)

    # Wait for 20 minutes
    time.sleep(60*2)
