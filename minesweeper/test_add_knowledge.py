import minesweeper as ms

def test_addknowledge7():
    """MinesweeperAI.add_knowledge can infer mine when given new information"""
    ai = ms.MinesweeperAI(height=4, width=5)
    ai.add_knowledge((2, 4), 1)
    ai.add_knowledge((2, 3), 1)
    ai.add_knowledge((1, 4), 0)
    ai.add_knowledge((3, 2), 0)
    expected = {(3, 4)}
    result = ai.mines
    if expected != result:
        print(f"mismatch: expected {expected}, result {result}")
    else:
        print("test_addknowledge7 passed")

def test_addknowledge8():
    """MinesweeperAI.add_knowledge can infer multiple mines when given new information"""
    ai = ms.MinesweeperAI(height=4, width=5)
    ai.add_knowledge((2, 0), 2)
    ai.add_knowledge((3, 1), 0)
    expected = {(1, 0), (1, 1)}
    result = ai.mines
    if expected != result:
        print(f"mismatch: expected {expected}, result {result}")
    else:
        print("test_addknowledge8 passed")

def test_addknowledge9():
    """MinesweeperAI.add_knowledge can infer safe cells when given new information"""
    ai = ms.MinesweeperAI(height=4, width=5)
    ai.add_knowledge((0, 1), 1)
    ai.add_knowledge((1, 0), 1)
    ai.add_knowledge((1, 2), 1)
    ai.add_knowledge((3, 1), 0)
    ai.add_knowledge((0, 4), 0)
    ai.add_knowledge((3, 4), 0)
    safes = [(0, 0), (0, 2)]
    for safe in safes:
        if safe not in ai.safes:
            print(f"did not find {safe} in safe cells when possible to conclude safe")
            break
    else:
        print("test_addknowledge9 passed")


def test_addknowledge10():
    """MinesweeperAI.add_knowledge combines multiple sentences to draw conclusions"""
    ai = ms.MinesweeperAI(height=4, width=5)
    ai.add_knowledge((3, 0), 2)
    ai.add_knowledge((2, 0), 3)
    ai.add_knowledge((1, 2), 1)
    mines = [(1, 0), (2, 1), (3, 1)]
    for mine in mines:
        if mine not in ai.mines:
            print(f"did not find {mine} in mines when possible to conclude mine")
            break
    else:
        print("test_addknowledge10 passed")


def main():
    test_addknowledge7()
    test_addknowledge8()
    test_addknowledge9()
    test_addknowledge10()

if __name__ == "__main__":
    main()