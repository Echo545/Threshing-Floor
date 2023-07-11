import sys
from hashlib import sha256

def read_key(filename):
    with open(filename, "r") as f:
        key = f.read()
    return key

def main():

    # check arguments
    if len(sys.argv) != 2:
        print("Usage: winnow.py <input_file>")
        sys.exit(1)

    INPUT_FILE = sys.argv[1]
    KEY_FILE = "KEY.txt"
    bits = []

    KEY = read_key(KEY_FILE)

    # Read input file into list of lines
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        serial, bit, mac = line.split(",")

        # Convert serial to int
        serial = int(serial, 16)

        mac_components = str(serial) + str(bit) + str(KEY)
        check_mac = sha256(mac_components.encode('utf-8')).hexdigest()

        if check_mac == mac:
            bits.append(bit)

    # Convert bits to chars
    chars = []
    for i in range(0, len(bits), 8):
        char_bits = bits[i:i+8]
        char = chr(int("".join(char_bits), 2))
        chars.append(char)

    print("".join(chars))


if __name__ == "__main__":
    main()