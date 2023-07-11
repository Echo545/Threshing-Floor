import sys

# Read target file name as argument

if len(sys.argv) != 2:
    print("Usage: intercept.py <input_file>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]

def bitsToChars(bits):
    chars = []
    for i in range(0, len(bits), 8):
        char_bits = bits[i:i+8]
        char = chr(int("".join(char_bits), 2))
        chars.append(char)
    return "".join(chars)

def main():
    # Read input file into list of lines
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    all_bits = []
    first_seen_bits = []
    last_seen_bits = []
    seen_serials = []

    # Iterate over lines
    for line in lines:

        line = line.strip()
        serial, bit, mac = line.split(",")
        serial = int(serial, 16)

        # Add bit to all_bits
        all_bits.append(bit)

        # Add bit to last_bits if serial has been seen before
        if serial in seen_serials:
            last_seen_bits.append(bit)

        # Add bit to first_bits if serial has not been seen before
        if serial not in seen_serials:
            first_seen_bits.append(bit)
            seen_serials.append(serial)

    # Convert bits to chars
    all_chars = bitsToChars(all_bits)
    first_chars = bitsToChars(first_seen_bits)
    last_chars = bitsToChars(last_seen_bits)

    print("---STATS---")

    # Print all lists of bits and their lengths
    print("Total number of bits read: " + str(len(all_bits)))
    print("First seen bits length: " + str(len(first_seen_bits)))
    print("Last seen bits length: " + str(len(last_seen_bits)))

    print("\n---RESULTS---")

    # Print all chars
    print("All chars: " + all_chars)
    print("First chars: " + first_chars)
    print("Last chars: " + last_chars)

if __name__ == "__main__":
    main()