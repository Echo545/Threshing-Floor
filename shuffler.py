import sys
import random

def main():

    if len(sys.argv) < 2:
        print("Usage: python shuffler.py <input file> <optional output file>")
        sys.exit(1)

    TARGET_FILE = sys.argv[1]
    output_file = TARGET_FILE

    # Specify output file if provided
    if len(sys.argv) == 3:
        output_file = sys.argv[2]

    with open(TARGET_FILE, 'r') as f:
        lines = f.readlines()

    # Handle newline chars
    lines = [line.strip() for line in lines]
    lines = [line + "\n" for line in lines]

    # Shuffle lines
    random.shuffle(lines)

    # Remove newline from last line
    lines[-1] = lines[-1].strip()

    with open(output_file, 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    main()