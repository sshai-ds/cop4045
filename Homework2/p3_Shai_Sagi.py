"""Homework 2, Problem 3: a simplified social network.

Sagi Shai

A social network is a dictionary mapping a username to a tuple
(full_name, [friend_username, ...]).
"""

import csv

from testif import testif


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a user with no friends to the social network.

    Args:
        sn: the social network dictionary.
        username: the new user's username.
        fullname: the new user's full name.

    Returns:
        True if the user was added, False if the username already existed.

    Raises:
        TypeError: if sn is not a dictionary.
    """
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except TypeError as err:
        print('Could not add user {}: {}'.format(username, err))
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual friend link between two users.

    Args:
        sn: the social network dictionary.
        user1: username of the first user.
        user2: username of the second user.

    Returns:
        True on success, False if either username is missing or they
        are the same user.

    Raises:
        TypeError: if sn is not a dictionary.
    """
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except TypeError as err:
        print('Could not link {} and {}: {}'.format(user1, user2, err))
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Return all friends of a user up to a given link distance.

    A breadth first search visits each user once, which avoids cycles.

    Args:
        sn: the social network dictionary.
        user1: the username to start from.
        distance: the maximum link distance, a positive integer.

    Returns:
        A list of usernames, closest first. Empty if the user is
        unknown or has no friends within that distance.

    Raises:
        TypeError: if sn is not a dictionary.
    """
    try:
        if user1 not in sn or distance < 1:
            return []
        found = []
        visited = {user1}
        frontier = [user1]
        for _ in range(distance):
            next_frontier = []
            for person in frontier:
                for friend in sn[person][1]:
                    if friend not in visited:
                        visited.add(friend)
                        found.append(friend)
                        next_frontier.append(friend)
            frontier = next_frontier
        return found
    except TypeError as err:
        print('Could not search from {}: {}'.format(user1, err))
        raise


def save_network(filename: str, sn: dict) -> None:
    """Save a social network to a CSV file.

    Each row holds the username, the full name, then the friends.

    Args:
        filename: name of the CSV file to write.
        sn: the social network dictionary.

    Raises:
        OSError: if the file cannot be written.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        for username in sorted(sn):
            fullname, friends = sn[username]
            writer.writerow([username, fullname] + friends)


def load_network(filename: str) -> dict:
    """Load a social network from a CSV file written by save_network.

    Args:
        filename: name of the CSV file to read.

    Returns:
        The social network dictionary.

    Raises:
        OSError: if the file cannot be read.
    """
    sn = {}
    with open(filename, 'r', newline='', encoding='utf-8') as source:
        for row in csv.reader(source):
            if row:
                sn[row[0]] = (row[1], row[2:])
    return sn


def build_sample() -> dict:
    """Return the sample network from the assignment."""
    sn = {}
    add_user(sn, 'alice', 'Alice Smith')
    add_user(sn, 'maria', 'Maria Cortez')
    add_user(sn, 'joe', 'Joseph Adams')
    add_user(sn, 'eve', 'Evelyn Cooper')
    add_user(sn, 'david', 'David Benson')
    add_friend(sn, 'alice', 'maria')
    add_friend(sn, 'maria', 'joe')
    add_friend(sn, 'maria', 'david')
    add_friend(sn, 'joe', 'eve')
    return sn


def test() -> None:
    """Extra credit: test parts a to e with testif from Module 2."""
    print('--- testif tests ---')

    sn = {}
    testif(add_user(sn, 'alice', 'Alice Smith'), 'add_user new',
           'alice was added', 'a new user was rejected')
    testif(not add_user(sn, 'alice', 'Alice Again'), 'add_user duplicate',
           'the duplicate was rejected', 'a duplicate username was allowed')

    add_user(sn, 'maria', 'Maria Cortez')
    testif(add_friend(sn, 'alice', 'maria'), 'add_friend valid',
           'alice and maria are linked', 'a valid link was rejected')
    testif(not add_friend(sn, 'alice', 'nobody'), 'add_friend missing user',
           'the missing user was rejected', 'a missing user was allowed')

    sample = build_sample()
    testif(get_friends(sample, 'alice', 1) == ['maria'],
           'get_friends distance 1', 'returned [maria]', 'wrong list returned')
    testif(sorted(get_friends(sample, 'alice', 2)) == ['david', 'joe', 'maria'],
           'get_friends distance 2', 'returned maria, joe, david',
           'wrong list returned')
    testif(get_friends(sample, 'nobody', 2) == [],
           'get_friends unknown user', 'returned the empty list',
           'an unknown user did not return []')

    save_network('network_test.csv', sample)
    testif(load_network('network_test.csv') == sample,
           'save and load round trip', 'the network survived the round trip',
           'the round trip changed the network')
    print()


def main() -> None:
    """Test every function in this module."""
    print('Sagi Shai - Homework 2, Problem 3')
    print()

    sn = build_sample()
    print('a) network after add_user calls:')
    for username in sorted(sn):
        print('  ', username, sn[username])
    print()

    print('b) add_friend(sn, "alice", "joe") ->', add_friend(sn, 'alice', 'joe'))
    print('   add_friend(sn, "alice", "nobody") ->', add_friend(sn, 'alice', 'nobody'))
    sn = build_sample()
    print()

    print('c) get_friends(sn, "alice", 1) ->', get_friends(sn, 'alice', 1))
    print('   get_friends(sn, "alice", 2) ->', get_friends(sn, 'alice', 2))
    print('   get_friends(sn, "alice", 3) ->', get_friends(sn, 'alice', 3))
    print('   get_friends(sn, "nobody", 2) ->', get_friends(sn, 'nobody', 2))
    print()

    print('d) saving to network.csv')
    save_network('network.csv', sn)
    with open('network.csv', 'r', encoding='utf-8') as saved:
        print(saved.read(), end='')
    print()

    print('e) loading it back')
    loaded = load_network('network.csv')
    print('   loaded network equals the original:', loaded == sn)
    print()

    try:
        load_network('does_not_exist.csv')
    except OSError as err:
        print('   expected error for a missing file:', err)
    print()

    test()


if __name__ == '__main__':
    main()
