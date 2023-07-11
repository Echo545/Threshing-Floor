# Threshing Floor

Simple implementation of chaffing and winnowing as described by Ronald L. Rivest in this paper: [Chaffing and Winnowing: Confidentiality without Encryption](https://people.csail.mit.edu/rivest/pubs/Riv98a.pdf)

## Usage

Set your own 64 character key in `KEY.txt` or leave it as the default key.

To create a formatted wheat file run `python wheat.py <message>`. This will create `wheat.txt`

Once a wheat file has been created, add chaff by running `python chaff.py`. This will output `chaffed.txt`

To read a message authenticated by the key in `KEY.txt` run `python winnow.py <message file>`. If the example is followed correctly, running `python winnow.py wheat.txt` or `python winnow.py chaffed.txt` should yield the same result.