"""Problem 4: non-interactive text editor functions for utf-8 text files.

File I/O errors are not caught; they pass to the
caller.
"""
import os

from testif import testif


def _read_text(filename: str) -> str:
    """Return the whole content of a utf-8 text file."""
    with open(filename, encoding="utf-8") as f:
        return f.read()


def _write_text(filename: str, text: str) -> None:
    """Overwrite a utf-8 text file with text."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def _find_all(text: str, search_str: str) -> list[int]:
    """Return every index in text where search_str starts."""
    positions = []
    index = text.find(search_str)
    while index != -1:
        positions.append(index)
        index = text.find(search_str, index + 1)
    return positions


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Return the file content in the half-open range [from_, to).

    to == -1 means the end of the file. from_ has an underscore because
    from is a Python keyword.
    Raises: IndexError if to exceeds the file length or the range is
        invalid.
    """
    text = _read_text(filename)
    if to == -1:
        to = len(text)
    if not 0 <= from_ <= to <= len(text):
        raise IndexError(f"invalid range [{from_}, {to}) for file length "
                         f"{len(text)}")
    return text[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Return the positions of search_str in the file, or [] if not found.

    Raises: ValueError if search_str is empty.
    """
    if not search_str:
        raise ValueError("search_str must not be empty")
    return _find_all(_read_text(filename), search_str)


def ed_replace(filename: str, search_str: str, replace_with: str,
               occurrence: int = -1) -> int:
    """Replace search_str with replace_with in the file.

    occurrence == -1 replaces all occurrences; occurrence >= 0 replaces
    only that one (0 is the first).
    Postcondition: returns the number of replacements; the file is not
        changed if that number is 0.
    Raises: ValueError if search_str is empty or occurrence < -1.
    """
    if not search_str or occurrence < -1:
        raise ValueError("need a non-empty search_str and occurrence >= -1")
    text = _read_text(filename)
    if occurrence == -1:
        count = text.count(search_str)
        new_text = text.replace(search_str, replace_with)
    else:
        positions = _find_all(text, search_str)
        if occurrence >= len(positions):
            return 0
        start = positions[occurrence]
        new_text = (text[:start] + replace_with
                    + text[start + len(search_str):])
        count = 1
    if count:
        _write_text(filename, new_text)
    return count


def ed_append(filename: str, string: str) -> int:
    """Append string to the file, creating the file if it doesn't exist.

    Postcondition: returns the number of characters written.
    """
    with open(filename, "a", encoding="utf-8") as f:
        return f.write(string)


def test_ed_find() -> None:
    """Unit tests for ed_find()."""
    fn = "test_find.txt"
    _write_text(fn, "01234567890123456789")
    testif(ed_find(fn, "345") == [3, 13], "ed_find two matches", "[3, 13]",
           "wrong positions")
    testif(ed_find(fn, "356") == [], "ed_find no match", "[]",
           "should be []")
    testif(ed_find(fn, "0") == [0, 10], "ed_find one character", "[0, 10]",
           "wrong positions")
    os.remove(fn)


def test_ed_replace() -> None:
    """Unit tests for ed_replace()."""
    fn = "test_replace.txt"
    _write_text(fn, "01234567890123456789")
    count = ed_replace(fn, "345", "ABCDE", 1)
    testif(count == 1 and _read_text(fn) == "0123456789012ABCDE6789",
           "ed_replace second occurrence", "replaced", "wrong result")

    _write_text(fn, "01234567890123456789")
    count = ed_replace(fn, "345", "ABCDE")
    testif(count == 2 and _read_text(fn) == "012ABCDE6789012ABCDE6789",
           "ed_replace all", "both replaced", "wrong result")

    count = ed_replace(fn, "ABCDE", "345", 5)
    testif(count == 0 and _read_text(fn) == "012ABCDE6789012ABCDE6789",
           "ed_replace occurrence too large", "file unchanged",
           "file changed")
    os.remove(fn)


def main() -> None:
    """Show how to use every ed_ function, then run the unit tests."""
    fn = "file1.txt"
    if os.path.exists(fn):
        os.remove(fn)

    print("ed_append(fn, '0123456789') ->", ed_append(fn, "0123456789"))
    print("ed_append(fn, '0123456789') ->", ed_append(fn, "0123456789"))
    print("ed_read(fn, 3, 9) ->", ed_read(fn, 3, 9))
    print("ed_read(fn, 3) ->", ed_read(fn, 3))
    print("ed_find(fn, '345') ->", ed_find(fn, "345"))
    print("ed_find(fn, '356') ->", ed_find(fn, "356"))
    print("ed_replace(fn, '345', 'ABCDE', 1) ->",
          ed_replace(fn, "345", "ABCDE", 1), "| file:", ed_read(fn))
    _write_text(fn, "01234567890123456789")
    print("ed_replace(fn, '345', 'ABCDE') ->",
          ed_replace(fn, "345", "ABCDE"), "| file:", ed_read(fn))

    print("\nUnit tests:")
    test_ed_find()
    test_ed_replace()


if __name__ == "__main__":
    main()
