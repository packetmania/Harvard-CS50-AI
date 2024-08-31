import sys
import generate

def ac3_4():
    """ac3 handles multiple rounds of updates"""

    # Setup
    sys.path = [""] + sys.path
    Var = generate.Variable
    crossword = generate.Crossword("data/structure3.txt", "data/words3.txt")
    creator = generate.CrosswordCreator(crossword)

    # Action
    creator.domains = {
        Var(0, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "SLOPE", "GRANT", "WHERE", "CLOTH"},
        Var(0, 2, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(2, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "SLOPE", "GRANT", "WHERE", "CLOTH"},
        Var(2, 4, "down", 3): {"RAM", "AIL", "PAN", "RAT"},
        Var(4, 1, "across", 5): {"FRONT", "AMAZE", "DAISY", "SLOPE", "GRANT", "WHERE", "CLOTH"}
    }
    expected = {
        Var(0, 1, "across", 5): {"DAISY"},
        Var(0, 2, "down", 3): {"AIL"},
        Var(2, 1, "across", 5): {"SLOPE"},
        Var(2, 4, "down", 3): {"PAN"},
        Var(4, 1, "across", 5): {"GRANT", "FRONT"}
    }
    creator.ac3()
    ret = True
    for var in expected:
        if expected[var] != creator.domains[var]:
            print(f"Expected: {expected[var]}, Got: {creator.domains[var]}")
            ret = False
    return ret


def main():
    if ac3_4():
        print("\nAC-3 test passed!")
    else:
        print("\nAC-3 test failed!")

if __name__ == "__main__":
    main()