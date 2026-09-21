"""Homework 2, Problem 1: parsing Python source files.

Sagi Shai
"""


def line_number(source_file: str, dest_file: str) -> None:
    """Copy a text file, prefixing every line with its line number.

    Args:
        source_file: name of the text file to read.
        dest_file: name of the file to write. It is overwritten.

    Raises:
        OSError: if either file cannot be opened.
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as src:
            lines = src.readlines()
        with open(dest_file, 'w', encoding='utf-8') as dest:
            for number, line in enumerate(lines, start=1):
                dest.write('{} {}'.format(number, line))
    except OSError as err:
        print('Could not number lines from {}: {}'.format(source_file, err))
        raise


def strip_comment(line: str) -> str:
    """Remove a trailing # comment from a line of Python code.

    A # inside a string literal is not a comment, so quotes are tracked.

    Args:
        line: one line of Python source.

    Returns:
        The line with any comment removed and trailing spaces stripped.
    """
    quote = ''
    for index, char in enumerate(line):
        if quote:
            if char == quote:
                quote = ''
        elif char in '\'"':
            quote = char
        elif char == '#':
            return line[:index].rstrip()
    return line.rstrip()


def indent_of(line: str) -> int:
    """Return the number of leading spaces in a line."""
    return len(line) - len(line.lstrip())


def parse_functions(filename: str) -> tuple:
    """Parse a Python file and return information about its functions.

    Args:
        filename: name of the .py file to parse.

    Returns:
        A tuple of tuples, each holding the line number of the def, the
        function name, the formal argument list as a string, and the
        function code as a string with comments and blank lines removed.
        The outer tuple is ordered alphabetically by function name.

    Raises:
        OSError: if the file cannot be opened.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as source:
            lines = source.readlines()
    except OSError as err:
        print('Could not parse {}: {}'.format(filename, err))
        raise

    functions = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip()
        if stripped.startswith('def '):
            header_indent = indent_of(line)
            name = stripped[4:stripped.find('(')].strip()
            args = stripped[stripped.find('(') + 1:stripped.rfind(')')].strip()

            code_lines = [strip_comment(line)]
            body = index + 1
            while body < len(lines):
                current = lines[body]
                if current.strip() and indent_of(current) <= header_indent:
                    break
                cleaned = strip_comment(current)
                if cleaned.strip():
                    code_lines.append(cleaned)
                body += 1

            functions.append((index + 1, name, args, '\n'.join(code_lines) + '\n'))
            index = body
        else:
            index += 1

    functions.sort(key=lambda item: item[1])
    return tuple(functions)


def main() -> None:
    """Test line_number and parse_functions on this source file."""
    this_file = 'p1_Shai_Sagi.py'
    output_file = 'p1_Shai_Sagi.py.txt'

    print('Sagi Shai - Homework 2, Problem 1')
    print()

    print('Part a: writing numbered lines to', output_file)
    line_number(this_file, output_file)
    with open(output_file, 'r', encoding='utf-8') as numbered:
        for line in numbered.readlines()[:8]:
            print(line, end='')
    print('...')
    print()

    print('Part b: functions found in', this_file)
    for entry in parse_functions(this_file):
        print('line {}, name {}, args ({})'.format(entry[0], entry[1], entry[2]))
        print(entry[3])


if __name__ == '__main__':
    main()
