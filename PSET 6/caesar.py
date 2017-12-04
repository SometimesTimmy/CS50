import cs50
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: caesar.py k")
        exit(1)

    if len(sys.argv) == 2:
        key = int(sys.argv[1])
        key = key%26
        print("plaintext:  ", end="")
        plain = cs50.get_string() # plain asks for "p"lain text
        print("ciphertext: ", end="")

    if plain != None:
        n = len(plain)
        for char in plain: #sweep the length of plain text
            if not char.isalpha(): # if it is not a letter, re-print as is
                print(char, end="")
            if char.isupper():
                print(chr((ord(char)-65+key)%26+65), end="")
                # https://stackoverflow.com/questions/227459/ascii-value-of-a-character-in-python
                # ord() to convert from char to int
                # chr() to convert int back to char
            if char.islower():
                print(chr((ord(char)-95+key)%26+65), end="")
        print("")
    exit(0)

if __name__ == "__main__":
    main()