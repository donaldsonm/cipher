from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Split string into individual lines
    set_a = set(a.splitlines())
    set_b = set(b.splitlines())

    # Find strings that the set has in commmon
    line_similarities = set_a & set_b
    return line_similarities


def sentences(a, b):
    """Return sentences in both a and b"""

    # Split string into individual sentences
    set_a = set(sent_tokenize(a))
    set_b = set(sent_tokenize(b))

    # Find strings that the set has in common
    sentence_similarities = set_a & set_b
    return sentence_similarities


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # Split string into substrings
    set_a = set()
    set_b = set()
    for i in range(len(a) - n + 1):
        set_a.add(a[i:n + i])
    for k in range(len(b) - n + 1):
        set_b.add(b[k:n + k])

    # Find strings that the set has in common
    substring_similarities = set_a & set_b
    return substring_similarities