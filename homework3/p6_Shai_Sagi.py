"""Problem 6: estimate storage used by nested folders and files."""
from __future__ import annotations

import unittest


class Entry:
    """Base class for a file-system entry with a name and optional parent."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an entry with its name and parent folder."""
        self.name = name
        self._parent = parent

    def parent(self) -> Entry | None:
        """Return this entry's parent, or None if it is a root entry."""
        return self._parent

    def size(self) -> int:
        """Return the entry's size in bytes."""
        raise NotImplementedError("Entry subclasses must implement size()")

    def absolute_path(self) -> list[Entry]:
        """Return this entry followed by its ancestors up to the root."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()


class File(Entry):
    """A file entry whose size is a nonnegative number of bytes."""

    def __init__(self, name: str, bytes_used: int,
                 parent: Entry | None = None) -> None:
        """Initialize a file and reject negative storage sizes."""
        super().__init__(name, parent)
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative")
        self.bytes_used = bytes_used

    def size(self) -> int:
        """Return the number of bytes used by this file."""
        return self.bytes_used


class Folder(Entry):
    """A folder entry containing files and other folders."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an empty folder."""
        super().__init__(name, parent)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add entry as a child and set its parent to this folder."""
        entry._parent = self
        self._children.append(entry)

    def size(self) -> int:
        """Return the total size of all files contained in this folder."""
        return sum(child.size() for child in self._children)

    def children(self) -> tuple[Entry, ...]:
        """Return this folder's children as an immutable tuple."""
        return tuple(self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Return files at least minimum_size bytes starting at entry.

    If entry is a file, return it when its size meets the threshold, or an
    empty list otherwise. If entry is a folder, search all of its descendants
    and return every qualifying file.
    """
    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    if isinstance(entry, Folder):
        return [
            file
            for child in entry.children()
            for file in find_large_files(child, minimum_size)
        ]
    return []


class EntryTests(unittest.TestCase):
    """Unit tests for recursive file search and absolute paths."""

    def setUp(self) -> None:
        """Create a three-level folder tree used by the tests."""
        self.root = Folder("root")
        self.documents = Folder("documents")
        self.archive = Folder("archive")
        self.root.add(self.documents)
        self.documents.add(self.archive)
        self.small_file = File("small.txt", 10)
        self.large_file = File("large.txt", 100)
        self.archive.add(self.small_file)
        self.root.add(self.large_file)

    def test_find_large_files_from_folder(self) -> None:
        """Find qualifying files recursively within a folder."""
        self.assertEqual(find_large_files(self.root, 50), [self.large_file])
        self.assertEqual(
            find_large_files(self.root, 10),
            [self.small_file, self.large_file],
        )

    def test_find_large_files_from_file(self) -> None:
        """Search a file entry directly and honor its size threshold."""
        self.assertEqual(find_large_files(self.large_file, 100),
                         [self.large_file])
        self.assertEqual(find_large_files(self.large_file, 101), [])

    def test_absolute_path(self) -> None:
        """Return a file's ancestors in entry-to-root order."""
        self.assertEqual(
            self.small_file.absolute_path(),
            [self.small_file, self.archive, self.documents, self.root],
        )
        self.assertEqual(self.root.absolute_path(), [self.root])


def main() -> None:
    """Demonstrate nested folder sizes, large-file search, and paths."""
    root = Folder("university")
    courses = Folder("courses")
    computer_science = Folder("computer_science")
    projects = Folder("projects")
    root.add(courses)
    courses.add(computer_science)
    computer_science.add(projects)
    projects.add(File("report.pdf", 1200))
    projects.add(File("dataset.csv", 5200))
    computer_science.add(File("notes.txt", 400))
    courses.add(File("schedule.txt", 100))

    print(f"Total size of {root.name}: {root.size()} bytes")
    for threshold in (1000, 5000):
        large_files = find_large_files(root, threshold)
        print(f"Files at least {threshold} bytes: "
              f"{[(file.name, file.size()) for file in large_files]}")

    report = projects.children()[0]
    print("Absolute path, entry to root:",
          " -> ".join(entry.name for entry in report.absolute_path()))


if __name__ == "__main__":
    main()
