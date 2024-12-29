import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP CNV
AJP -> Adj | Adj AJP
PP -> P NP | P NP Adv
NP -> N | Det N | Det N PP | Det AJP N | N PP
VP -> V | Adv VP | V Adv | V NP | V NP PP | V PP
CNV -> Conj NP VP | Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # raise NotImplementedError
    # Tokenize the sentence
    tokens = nltk.tokenize.word_tokenize(sentence)

    # Filter tokens: include only words with at least one alphabet character
    filtered_tokens = [word.lower() for word in tokens if any(char.isalpha() for char in word)]
    return filtered_tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # raise NotImplementedError
    np_chunks = []

    for subtree in tree.subtrees():
        # Check if the subtree is labeled "NP"
        if subtree.label() == "NP":
            # Ensure no nested "NP" subtree exists within any descendant
            contains_nested_np = any(
                descendant.label() == "NP" for descendant in subtree.subtrees() if descendant != subtree
            )
            if not contains_nested_np:
                np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
