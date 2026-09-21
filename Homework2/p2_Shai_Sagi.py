"""Homework 2, Problem 2: list and dictionary comprehensions.

Sagi Shai
"""


def main() -> None:
    """Run every comprehension and display its result."""
    print('Sagi Shai - Homework 2, Problem 2')
    print()

    # a) Distinct a, b, c, d in 1..10 with a*a + b*b == c*c + d*d.
    quads = [(a, b, c, d)
             for a in range(1, 11)
             for b in range(1, 11)
             for c in range(1, 11)
             for d in range(1, 11)
             if len({a, b, c, d}) == 4 and a * a + b * b == c * c + d * d]
    print('a) count =', len(quads))
    print('   first 5:', quads[:5])
    print()

    # b) Lowercase word and its length, only for words shorter than five.
    words = ['One', 'SEVEN', 'three', 'two', 'Ten']
    short = [(word.lower(), len(word)) for word in words if len(word) < 5]
    print('b)', short)
    print()

    # c) Full names reformatted as Firstname M. Lastname.
    names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    initials = ['{} {}. {}'.format(parts[0], parts[1][0], parts[2])
                for parts in (name.split() for name in names)]
    print('c)', initials)
    print()

    # d) Anagram pairs across two lists, case insensitive.
    lst1 = ['Spam', 'Trams', 'Elbows', 'Tops', 'Astral']
    lst2 = ['Bowels', 'Sample', 'Altars', 'Stop', 'Course', 'Smart']
    anagrams = [(w1, w2) for w1 in lst1 for w2 in lst2
                if sorted(w1.lower()) == sorted(w2.lower())]
    print('d)', anagrams)
    print()

    # e) Map each string to its length.
    s = ['one', 'two', 'three']
    lengths = {word: len(word) for word in s}
    print('e)', lengths)
    print()

    # f) Map the index of every vowel to that vowel.
    text = 'Hello world'
    vowels = {index: char for index, char in enumerate(text)
              if char.lower() in 'aeiou'}
    print('f)', vowels)


if __name__ == '__main__':
    main()
