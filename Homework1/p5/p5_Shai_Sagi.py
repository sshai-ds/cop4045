LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesar_cipher(text, shift):
    result = ""

    for character in text:
        if character in LOWERCASE:
            index = LOWERCASE.index(character)
            result += LOWERCASE[(index + shift) % 26]
        elif character in UPPERCASE:
            index = UPPERCASE.index(character)
            result += UPPERCASE[(index + shift) % 26]
        else:
            result += character

    return result


def caesar_decipher(cyphertext, shift):
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    frequencies = {}

    for letter in LOWERCASE:
        frequencies[letter] = 0

    for character in text.lower():
        if character in LOWERCASE:
            frequencies[character] += 1

    return frequencies


def main():
    while True:
        print("\n1. Encrypt and analyze")
        print("2. Quit")
        choice = input("Choose an option: ")

        if choice == "2":
            break
        if choice != "1":
            print("Invalid option")
            continue

        message = input("Enter a message: ")
        shift = int(input("Enter a shift value: "))
        ciphered = caesar_cipher(message, shift)
        deciphered = caesar_decipher(ciphered, shift)

        print("Ciphered text:", ciphered)
        print("Letter frequencies:")
        for letter, count in letter_frequency(message).items():
            print("{}: {}".format(letter, count))
        print("Deciphered text:", deciphered)


if __name__ == "__main__":
    main()
