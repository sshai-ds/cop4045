"""Problem 5: recursion - leaves, base conversion, n-choose-k, pairs."""
from __future__ import annotations

import time
import turtle
from collections.abc import Sequence

from testif import testif

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cnk_memo: dict[tuple[int, int], int] = {}


def draw_leaf(level: int, length: float, bend: float = 0) -> None:
    """Recursively draw a leaf from the turtle's position and heading.

    length is the petiole length; bend turns each branching point right by
    that many degrees (0 draws a straight leaf).
    Precondition: level >= 0 and length > 0.
    Postcondition: the turtle is back at its start position and heading.
    """
    turtle.forward(length)
    if level > 0:
        turtle.right(bend)
        turtle.left(45)
        draw_leaf(level - 1, length * 0.4, bend)
        turtle.right(90)
        draw_leaf(level - 1, length * 0.4, bend)
        turtle.left(45)
        turtle.forward(length * 0.9)
        draw_leaf(level - 1, length * 0.6, bend)
        turtle.backward(length * 0.9)
        turtle.left(bend)
    turtle.backward(length)


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw a straight leaf; length is the petiole length."""
    draw_leaf(level, length)


def draw_leaf_curved(level: int, length: float) -> None:
    """Draw a leaf that curves to the right (extra credit)."""
    draw_leaf(level, length, bend=15)


def start_leaf(x: float, y: float, label: str) -> None:
    """Write label under (x, y), then move there with the turtle pointing
    up (turned left 90 degrees from East).
    """
    turtle.up()
    turtle.goto(x, y - 30)
    turtle.write(label, align="center", font=("Arial", 12, "normal"))
    turtle.goto(x, y)
    turtle.setheading(90)
    turtle.down()


def strB(n: int, base: int = 10) -> str:
    """Return n written in the given base, recursively.

    Digits above 9 are the letters 'A' to 'Z'.
    Raises: ValueError unless n >= 0 and 2 <= base <= 26.
    """
    if n < 0 or not 2 <= base <= 26:
        raise ValueError("need n >= 0 and 2 <= base <= 26")
    if n < base:
        return DIGITS[n]
    return strB(n // base, base) + DIGITS[n % base]


def Cnk_m(n: int, k: int) -> int:
    """Return n choose k, recursively, with memoization in cnk_memo.

    Raises: ValueError unless 0 <= k <= n.
    """
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")
    if k == 0 or k == n:
        return 1
    if (n, k) not in cnk_memo:
        cnk_memo[(n, k)] = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    return cnk_memo[(n, k)]


def run_Cnk(n: int, k: int) -> int:
    """Print and return Cnk_m(n, k) with the time it took."""
    start = time.perf_counter()
    value = Cnk_m(n, k)
    ms = (time.perf_counter() - start) * 1000
    print(f"Cnk_m({n}, {k}) = {value}  ({ms:.3f} ms)")
    return value


def make_pairs(seq1: Sequence, seq2: Sequence,
               acc: list[tuple] | None = None) -> list[tuple]:
    """Return a list of (seq1[i], seq2[i]) tuples, recursively.

    Stops at the end of the shorter sequence. acc is the accumulator;
    callers leave it out.
    """
    if acc is None:
        acc = []
    if not seq1 or not seq2:
        return acc
    return make_pairs(seq1[1:], seq2[1:], acc + [(seq1[0], seq2[0])])


def test_strB() -> None:
    """Four unit tests for strB()."""
    testif(strB(0) == "0", "strB(0)", "'0'", "wrong string")
    testif(strB(5, base=2) == "101", "strB(5, base=2)", "'101'",
           "wrong string")
    testif(strB(255, base=16) == "FF", "strB(255, base=16)", "'FF'",
           "wrong string")
    testif(strB(675, base=26) == "PP", "strB(675, base=26)", "'PP'",
           "wrong string")


def test_Cnk_m() -> None:
    """Four unit tests for Cnk_m()."""
    testif(Cnk_m(7, 0) == 1, "Cnk_m(7, 0)", "1", "wrong value")
    testif(Cnk_m(5, 2) == 10, "Cnk_m(5, 2)", "10", "wrong value")
    testif(Cnk_m(20, 10) == 184756, "Cnk_m(20, 10)", "184756",
           "wrong value")
    testif(Cnk_m(52, 5) == 2598960, "Cnk_m(52, 5)", "2598960",
           "wrong value")


def test_make_pairs() -> None:
    """Five unit tests for make_pairs(), including empty sequences."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)],
           "make_pairs same length", "3 pairs", "wrong pairs")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)],
           "make_pairs second shorter", "2 pairs", "wrong pairs")
    testif(make_pairs([1], [4, 5, 6]) == [(1, 4)],
           "make_pairs first shorter", "1 pair", "wrong pairs")
    testif(make_pairs([], [4, 5, 6]) == [], "make_pairs first empty", "[]",
           "should be []")
    testif(make_pairs([1, 2, 3], []) == [], "make_pairs second empty",
           "[]", "should be []")


def main() -> None:
    """Run the unit tests and run_Cnk(), then draw both leaves."""
    test_strB()
    test_Cnk_m()
    test_make_pairs()
    print()
    run_Cnk(10, 5)
    run_Cnk(30, 15)
    run_Cnk(100, 50)

    turtle.setup(1100, 750)
    turtle.hideturtle()
    turtle.tracer(0)
    start_leaf(-250, -300, "draw_leaf_straight(6, 120)")
    draw_leaf_straight(6, 120)
    start_leaf(230, -300, "draw_leaf_curved(6, 120)")
    draw_leaf_curved(6, 120)
    turtle.update()
    turtle.done()


if __name__ == "__main__":
    main()
