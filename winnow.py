import sys
from hashlib import sha256

# Reads key file
def readKey(filename):
    with open(filename, "r") as f:
        key = f.read()
    return key

# Concerts a list of bits to a string
def bitsToString(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int("".join(byte), 2)))
    return "".join(chars)

# Generates every possible combination of bits for a list with missing bits
def possibleResults(bits):
    workingStack = []
    results = []

    # Remove redundant trailing None values
    while bits[-1] == None and bits[-2] == None:
        bits.pop()

    workingStack.append(bits)

    while len(workingStack) > 0:
        current = workingStack.pop()

        if None not in current:
            results.append(current)
        else:
            index = current.index(None)
            current[index] = "0"
            workingStack.append(current.copy())
            current[index] = "1"
            workingStack.append(current.copy())

    return results

# Returns true if message hash is expected
def authenticMessage(serial, bit, mac, key):
    hash_components = str(serial) + str(bit) + str(key)
    hash = sha256(hash_components.encode('utf-8')).hexdigest()

    return hash == mac

# Returns the highest serial numbers in a list of lines
def maxValidSerial(lines, key):
    max_valid = 0

    for line in lines:
        serial, bit, mac = messageParts(line)

        if authenticMessage(serial, bit, mac, key):
            if serial > max_valid:
                max_valid = serial

    return max_valid

# Gets the serial, bit, and mac from a line
def messageParts(line):
    line = line.strip()

    if len(line) > 0:
        try:
            serial, bit, mac = line.split(",")
        except:
            print("Malformed file format. Expected format: <serial>,<bit>,<mac>")
            sys.exit(1)

        serial = int(serial, 16)
    return serial, bit, mac

def main():
    # check arguments
    if len(sys.argv) < 2:
        print("Usage: winnow.py <input file> <attempt to brute force missing entries (T/F) default True>")
        sys.exit(1)

    bruteForce = True

    if len(sys.argv) == 3:
        if sys.argv[2] == "F" or sys.argv[2] == "f":
            bruteForce = False

    INPUT_FILE = sys.argv[1]
    KEY_FILE = "KEY.txt"
    KEY = readKey(KEY_FILE)

    # Read input file into list of lines
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    max_valid_serial = maxValidSerial(lines, KEY)
    bits = [None] * (max_valid_serial + 1)

    # Process lines
    for line in lines:
        line = line.strip()

        if len(line) > 0:
            try:
                serial, bit, mac = line.split(",")
            except:
                print("Malformed file format. Expected format: <serial>,<bit>,<mac>")
                sys.exit(1)

            serial = int(serial, 16)

            if authenticMessage(serial, bit, mac, KEY):
                bits[serial] = bit

    # Check for missing bits
    missing_bits = []
    for i in range(len(bits)):
        if bits[i] == None:
            missing_bits.append(i + 1)

    # Display results
    if len(bits) >= 8:
        if len(missing_bits) > 0:
            print("Missing messages at serial number(s): " + str(missing_bits))

            if bruteForce:
                options = possibleResults(bits)

                # Print every option
                print("Possible results:")
                for i, option in enumerate(options):
                    print("   " + str(i + 1) + ".", bitsToString(option))
            else:
                print("Brute force guessing disabled... Exiting.")
        else:
            print(bitsToString(bits))
    else:
        # Remove None values from bits
        while None in bits:
            bits.remove(None)

        print("Incomplete message/ no message found.")
        print("Valid bits received: " + str(len(bits)))

if __name__ == "__main__":
    main()