"""Homework 2, Problem 4: IMDB top rated and top grossing movies.

Sagi Shai

Reads three CSV files and displays two rankings:
  a) director and actor pairs who worked together on top rated movies,
  b) actors ranked by the box office of the top grossing movies they were in.
"""

import csv

RATED_FILE = 'imdb-top-rated.csv'
GROSSING_FILE = 'imdb-top-grossing.csv'
CASTS_FILE = 'imdb-top-casts.csv'


def movie_key(title: str, year: str) -> tuple:
    """Build the key used to match a movie across the three files.

    Args:
        title: the movie title.
        year: the release year as a string.

    Returns:
        A (title, year) tuple with whitespace stripped.
    """
    return (title.strip(), year.strip())


def read_movies(filename: str, value_column: int) -> dict:
    """Read a ranking file and map each movie to one column's value.

    Args:
        filename: the CSV file to read. It has a heading row.
        value_column: index of the column to keep, for example the
            rating column or the box office column.

    Returns:
        A dictionary mapping (title, year) to the raw column value.

    Raises:
        OSError: if the file cannot be read.
    """
    movies = {}
    try:
        with open(filename, 'r', encoding='utf-8') as source:
            reader = csv.reader(source)
            next(reader, None)  # skip the heading row
            for row in reader:
                if len(row) > value_column:
                    movies[movie_key(row[1], row[2])] = row[value_column]
    except OSError as err:
        print('Could not read {}: {}'.format(filename, err))
        raise
    return movies


def read_casts(filename: str) -> dict:
    """Read the cast file and map each movie to its director and actors.

    Args:
        filename: the CSV file to read. It has no heading row.

    Returns:
        A dictionary mapping (title, year) to (director, [actors]).

    Raises:
        OSError: if the file cannot be read.
    """
    casts = {}
    try:
        with open(filename, 'r', encoding='utf-8') as source:
            for row in csv.reader(source):
                if len(row) >= 4:
                    actors = [name.strip() for name in row[3:] if name.strip()]
                    casts[movie_key(row[0], row[1])] = (row[2].strip(), actors)
    except OSError as err:
        print('Could not read {}: {}'.format(filename, err))
        raise
    return casts


def parse_money(amount: str) -> float:
    """Convert a box office string such as $1,234,567 to a float.

    Args:
        amount: the raw box office text.

    Returns:
        The value as a float, or 0.0 if it cannot be read.
    """
    cleaned = amount.replace('$', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def display_ranking(title: str, rows: list, limit: int = None) -> None:
    """Print a ranking, optionally cut to the first few entries.

    Args:
        title: heading printed above the ranking.
        rows: list of tuples already sorted in display order.
        limit: maximum number of entries to print. None prints all.
    """
    print(title)
    shown = rows if limit is None else rows[:limit]
    for rank, row in enumerate(shown, start=1):
        print('{:3}. {}'.format(rank, row))
    print('   showing {} of {} entries'.format(len(shown), len(rows)))
    print()


def display_top_collaborations(limit: int = None) -> None:
    """Rank director and actor pairs by shared top rated movies.

    Args:
        limit: maximum number of entries to print. None prints all.
    """
    rated = read_movies(RATED_FILE, 3)
    casts = read_casts(CASTS_FILE)

    counts = {}
    for key in rated:
        if key in casts:
            director, actors = casts[key]
            for actor in actors:
                pair = (director, actor)
                counts[pair] = counts.get(pair, 0) + 1

    ranking = [(director, actor, total)
               for (director, actor), total in counts.items()]
    ranking.sort(key=lambda row: row[2], reverse=True)
    display_ranking('a) Top director and actor collaborations', ranking, limit)


def display_top_actors(limit: int = None) -> None:
    """Rank actors by the total box office of their top grossing movies.

    Args:
        limit: maximum number of entries to print. None prints all.
    """
    grossing = read_movies(GROSSING_FILE, 3)
    casts = read_casts(CASTS_FILE)

    totals = {}
    for key, box_office in grossing.items():
        if key in casts:
            money = parse_money(box_office)
            for actor in casts[key][1]:
                totals[actor] = totals.get(actor, 0.0) + money

    ranking = [(actor, total) for actor, total in totals.items()]
    ranking.sort(key=lambda row: row[1], reverse=True)
    display_ranking('b) Top actors by box office', ranking, limit)


def main() -> None:
    """Test parts a and b, cutting each ranking to ten entries."""
    print('Sagi Shai - Homework 2, Problem 4')
    print()
    try:
        display_top_collaborations(limit=10)
        display_top_actors(limit=10)
    except OSError:
        print('Make sure the three CSV files are in this folder.')


if __name__ == '__main__':
    main()
