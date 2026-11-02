"""Problem 1: NVector, an N-dimensional vector of real numbers."""
from __future__ import annotations

from collections.abc import Sequence

from testif import testif


class NVector:
    """N-dimensional vector of real numbers stored in a list."""

    def __init__(self, *args: float | Sequence[float]) -> None:
        """Create a vector from one sequence, or from two or more numbers.

        Postcondition: the elements are copied into a new list.
        Raises: TypeError if a single argument is not a sequence.
        """
        if len(args) == 1:
            self.elements = list(args[0])
        else:
            self.elements = list(args)

    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self.elements)

    def __getitem__(self, index: int) -> float:
        """Return the element at index; negative indexes work like lists.

        Raises: IndexError if index is out of range.
        """
        return self.elements[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Set the element at index to value; negative indexes work too.

        Raises: IndexError if index is out of range.
        """
        self.elements[index] = value

    def __str__(self) -> str:
        """Return the vector as a string, e.g. 'NVector([3, 0, 1, -1])'."""
        return f"NVector({self.elements})"

    def __eq__(self, other: object) -> bool:
        """Return True if other is an NVector with the same elements."""
        return isinstance(other, NVector) and self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Return True if self and other are not equal."""
        return not self == other

    def __add__(self, other: NVector | float) -> NVector:
        """Add an NVector element-wise, or add a number to every element.

        Postcondition: returns a new NVector; self is unchanged.
        Raises: ValueError if the vectors have different lengths.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("vectors must have the same length")
            pairs = zip(self.elements, other.elements)
            return NVector([a + b for a, b in pairs])
        return NVector([a + other for a in self.elements])

    def __radd__(self, other: float) -> NVector:
        """Return other + self, used when the number is on the left."""
        return self + other

    def __mul__(self, other: NVector | float) -> float:
        """Multiply by an NVector or a number; the result is a number.

        A * B = sum(A[i] * B[i]) if B is an NVector, else sum(A[i] * B).
        Raises: ValueError if the vectors have different lengths.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("vectors must have the same length")
            return sum(a * b for a, b in zip(self.elements, other.elements))
        return sum(a * other for a in self.elements)

    def __rmul__(self, other: float) -> float:
        """Return other * self, used when the number is on the left."""
        return self * other

    @classmethod
    def zeros(cls, n: int) -> NVector:
        """Return a new n-dimensional NVector with all elements 0."""
        return cls([0] * n)


def main() -> None:
    """Test parts a) to j) with testif()."""
    data = [3, 0, 1, -1]
    v = NVector(data)
    u = NVector(1, 2, 3, 4)
    testif(v.elements == data and v.elements is not data, "a) NVector(list)",
           "elements copied to a new list", "list not copied")
    testif(NVector((3, 0, 1, -1)) == v, "a) NVector(tuple)", str(v),
           "wrong elements")
    testif(NVector(3, 0, 1, -1) == v, "b) NVector(3, 0, 1, -1)", str(v),
           "wrong elements")
    testif(len(v) == 4, "c) len(v)", "4", "wrong length")
    testif(v[1] == 0 and v[-2] == 1, "d) v[1], v[-2]", "0, 1",
           "wrong element")
    w = NVector(3, 0, 1, -1)
    w[2] = 5
    testif(w == NVector(3, 0, 5, -1), "e) w[2] = 5", str(w), "wrong element")
    testif(str(v) == "NVector([3, 0, 1, -1])", "f) str(v)", str(v),
           "wrong string")
    testif(v == NVector([3, 0, 1, -1]), "g) v == NVector([3, 0, 1, -1])",
           "equal", "not equal")
    testif(v != u, "g) v != u", "not equal", "equal")
    testif(v + u == NVector(4, 2, 4, 3), "h) v + u", str(v + u), "wrong sum")
    testif(v + 10 == NVector(13, 10, 11, 9), "h) v + 10", str(v + 10),
           "wrong sum")
    testif(10 + v == NVector(13, 10, 11, 9), "h) 10 + v", str(10 + v),
           "wrong sum")
    testif(v * u == 2, "i) v * u", "2", "wrong product")
    testif(v * 2 == 6, "i) v * 2", "6", "wrong product")
    testif(2 * v == 6, "i) 2 * v", "6", "wrong product")
    testif(NVector.zeros(3) == NVector(0, 0, 0), "j) NVector.zeros(3)",
           str(NVector.zeros(3)), "wrong vector")


if __name__ == "__main__":
    main()
