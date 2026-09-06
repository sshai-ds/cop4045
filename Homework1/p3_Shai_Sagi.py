def find_dup_str(s, n):
    if n<=0:
        return ""

    for first in range(len(s) - n + 1):
        substring=s[first:first + n]

        for second in range(first + n, len(s) - n + 1):
            if substring==s[second:second + n]:
                return substring

    return ""


def find_max_dup(s):
    for length in range(len(s) // 2, 0, -1):
        substring = find_dup_str(s, length)
        if substring != "":
            return substring

    return ""


def main():
    s=input("Enter a string: ")
    n=int(input("Enter a substring length: "))
    print(find_dup_str(s, n))

    s=input("Enter a string: ")
    print(find_max_dup(s))


if __name__=="__main__":
    main()
