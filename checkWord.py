from uzwords import words
from difflib import get_close_matches


def checkWords(word, words=words):
    word = word.lower()
    matches = set(get_close_matches(word, words))  # Start with a set of close matches
    available = False

    if word in matches:  # Check if the exact word is in the matches
        available = True
        matches = {word}  # Keep matches as a set with the word
    else:
        if "ҳ" in word:
            word_with_x = word.replace("ҳ", "x")
            matches.update(
                get_close_matches(word_with_x, words)
            )  # Add more matches with 'x'
        if "x" in word:
            word_with_ҳ = word.replace("x", "ҳ")
            matches.update(
                get_close_matches(word_with_ҳ, words)
            )  # Add more matches with 'ҳ'

    return {"available": available, "matches": matches}


if __name__ == "__main__":
    print(checkWords("мулк"))
    print(checkWords("ҳато"))
    print(checkWords("тариҳ"))
