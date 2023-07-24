import sys

# Converts a list of bits to a string of chars, replacing non-printable chars with 0x7F
def bitsToString(bits):
    chars = []
    for i in range(0, len(bits), 8):
        char_bits = bits[i:i+8]
        char = chr(int("".join(char_bits), 2))

        # If char is not printable, replace with 0x7F
        if not char.isprintable():
            char = chr(0x7F)

        chars.append(char)
    return "".join(chars)

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

# Gets the message bits from a list of lines
def getBits(lines):
    bits = []

    for line in lines:
        line = line.strip()

        if len(line) > 0:
            serial, bit, mac = messageParts(line)
            bits.append(bit)

    return bits

# Reorder the lines by serial number, returns first_seen_lines and last_seen_lines
def reorderLines(lines):
    first_seen_lines = []
    last_seen_lines = []
    seen_serials = []

    for line in lines:
        line = line.strip()

        if len(line) > 0:
            serial, bit, mac = messageParts(line)

            # Add bit to last_bits if serial has been seen before
            if serial in seen_serials:
                last_seen_lines.append(line)

            # Add bit to first_bits if serial has not been seen before
            if serial not in seen_serials:
                first_seen_lines.append(line)
                seen_serials.append(serial)

    # Sort first_seen_lines and last_seen_lines by serial number
    first_seen_lines.sort(key=lambda x: int(x.split(",")[0], 16))
    last_seen_lines.sort(key=lambda x: int(x.split(",")[0], 16))

    return first_seen_lines, last_seen_lines

def main():
    # Read target file name as argument
    if len(sys.argv) != 2:
        print("Usage: intercept.py <input_file>")
        sys.exit(1)

    INPUT_FILE = sys.argv[1]

    # Read input file into list of lines
    with open(INPUT_FILE, "r") as f:
        raw_lines = f.readlines()

    first_seen_lines, last_seen_lines = reorderLines(raw_lines)
    first_seen_bits = getBits(first_seen_lines)
    first_chars = bitsToString(first_seen_bits)

    print("First seen bits length: " + str(len(first_seen_bits)))
    print("First chars: " + first_chars)

    # if there were multiples messages with the same serial num, analyze them
    if len(last_seen_lines) > 0:
        last_seen_bits = getBits(last_seen_lines)
        last_chars = bitsToString(last_seen_bits)
        print("Last seen bits length: " + str(len(last_seen_bits)))
        print("Last chars: " + last_chars)


if __name__ == "__main__":
    main()