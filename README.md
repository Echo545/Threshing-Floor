# Threshing Floor

Simple implementation of chaffing and winnowing as described by Ronald L. Rivest in this paper: [Chaffing and Winnowing: Confidentiality without Encryption](https://people.csail.mit.edu/rivest/pubs/Riv98a.pdf)

## Usage

Set your own key in `KEY.txt` or leave it as the default key.

To create a formatted wheat file run `python wheat.py <message>`. This will create `wheat.txt`

Once a wheat file has been created, add chaff by running `python chaff.py`. This will output `chaffed.txt`

To read a message authenticated by the key in `KEY.txt` run `python winnow.py <message file>`. If the example is followed correctly, running `python winnow.py wheat.txt` or `python winnow.py chaffed.txt` should yield the same result.

If one or more bits (determined by the serial number) are missing from the input, `winnow.py` will attempt to guess all possible results by brute forcing the potential missing bits. This may be computationally intense if many bits are missing. To disable this feature, run `python winnow.py <input file> F(alse)`.

## Analyzing the Results

Here's a simply way to test the confidentiality of your outputs:
1. Run `wheat.py` and `chaff.py` as normal. Check that it worked by running `winnow.py`, you should see your original message.
2. Now modify the contents of `KEY.txt` to anything other than it was originally.
3. Run `winnow.py` using either `wheat.txt` or `chaffed.txt` as the input file. If the key used to winnow is different than the key used to generate the "wheat", then the entire input will be considered "chaff" and no message will be printed.

To simulate messages arriving out of order, you can run `python shuffler.py <input file> <optional output file>` to randomly shuffle the order of the lines in a file. If no output file is specified the contents of the current file will be shuffled.

### analyze.py

`analyze.py` will read the message field of each line in the given file (which is a single bit) and attempt to reconstruct the original message. It will also try constructing messages using only the first occurrences and last occurrences of a each message (noted using the message serial number)
* Running `python analyze.py wheat.txt` will result in getting the original message back as there is no chaff.
* Running `python analyze.py chaffed.txt` will result in a nonsense output as it is impossible to distinguish the "chaff" from the "wheat."

Note that `analyze.py` does not currently support shuffled files.

## Next Steps

- [x] Add a simple analysis program to verify results.
- [x] Guess missing bits while winnowing
- [x] Handle shuffled inputs
- [ ] Update analyze.py to handle shuffled input and guess missing bits
- [ ] Restructure output to use blocks of bits per message instead of a single bit per message.
- [ ] Build an advanced analysis program that tries multiple approaches to guess the original message.
- [ ] Build a simple chat client using chaffing and winnowing.