import random
import string
from hashlib import sha256

WHEAT_FILE = "out/wheat.txt"
OUTPUT_FILE = "out/chaffed.txt"

def randomKey():
    key = ""
    for i in range(64):
        key += random.choice(string.hexdigits)
    return key

def main():
    # Read the wheat file into a list of lines
    with open(WHEAT_FILE, "r") as f:
        lines = f.readlines()

    with open(OUTPUT_FILE, "w") as f:
        for wheat in lines:

            wheat = wheat.strip()

            serial, bit, mac = wheat.split(",")
            chaff_bit = str(int(bit) ^ 1)

            # generate a random key 64 chars
            key = randomKey()

            mac_components = str(serial) + str(chaff_bit) + str(key)
            mac = sha256(mac_components.encode('utf-8')).hexdigest()

            chaff_line = ",".join([str(serial), str(chaff_bit), mac])

            # Randomly select if chaff line goes first
            CHAFF_FIRST = random.choice([True, False])

            if int(serial, 16) != 0:
                f.write("\n")

            if CHAFF_FIRST:
                f.write(chaff_line)
                f.write("\n" + wheat)
            else:
                f.write(wheat)
                f.write("\n" + chaff_line)

if __name__ == "__main__":
    main()