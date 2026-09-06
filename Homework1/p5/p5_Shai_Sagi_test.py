import unittest

from p5_Shai_Sagi import (
    caesar_cipher,
    caesar_decipher,
    letter_frequency,
)


class CaesarCipherTest(unittest.TestCase):
    def test_cipher_preserves_case_and_symbols(self):
        self.assertEqual(caesar_cipher("Hello, World!", 3),
                         "Khoor, Zruog!")

    def test_cipher_wraps_alphabet(self):
        self.assertEqual(caesar_cipher("Zebra", 2), "Bgdtc")

    def test_decipher(self):
        self.assertEqual(caesar_decipher("Khoor", 3), "Hello")

    def test_letter_frequency(self):
        counts = letter_frequency("Apple pie! 123")
        self.assertEqual(counts["a"], 1)
        self.assertEqual(counts["p"], 3)
        self.assertEqual(counts["e"], 2)
        self.assertEqual(counts["z"], 0)


if __name__ == "__main__":
    unittest.main()
