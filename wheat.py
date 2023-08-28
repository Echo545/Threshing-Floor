import sys
import hmac

if len(sys.argv) != 2:
    print("Usage: wheat.py <message>")
    sys.exit(1)

MESSAGE = sys.argv[1]
OUTPUT_FILE = "out/wheat.txt"
AUTH_KEY_FILE = "KEY.txt"

def read_key(filename):
    with open(filename, "r") as f:
        key = f.read()
    return key

def main():
    # Read the key from the file
    KEY = read_key(AUTH_KEY_FILE).encode()

    # Convert the message to a list of bits
    message_chars = [ord(c) for c in MESSAGE]
    message_bits = []
    for char in message_chars:
        message_bits += [int(b) for b in bin(char)[2:].zfill(8)]


    with open(OUTPUT_FILE, "w") as f:
        serial = 0

        for bit in message_bits:

            # calculate mac for each bit: mac = SHA256(serial, bit, key)
            mac_components = str(serial) + str(bit)
            mac = hmac.new(KEY, mac_components.encode(), "sha256").hexdigest()

            # encode serial as 32 bit hex string
            encoded_serial = hex(serial)[2:].zfill(8)

            # add new line if serial is not 0
            if serial != 0:
                f.write("\n")

            # write serial,bit,mac to file
            f.write(",".join([str(encoded_serial), str(bit), mac]))

            serial += 1

if __name__ == "__main__":
    main()