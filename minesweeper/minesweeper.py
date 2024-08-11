import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            # all cells are mines
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            # all cells are safe
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)  # for 1)
        self.mark_safe(cell)       # for 2)

        # Loop over all cells within one row and column
        new_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        # Update count if cell in bounds and is mine
                        count -= 1
                    elif (i, j) not in self.safes:
                        # Add undetermined cell to the sentence
                        new_cells.add((i, j))

        if new_cells:
            new_sentence = Sentence(new_cells, count)
            self.knowledge.append(new_sentence)  # for 3)

        # for 4) and 5)
        # Recursive function for knowledge update including inferring
        def update_knowledge():
            # Update the sets of safe cells and mines
            mines_safes_changed = False
            for sen in self.knowledge:
                new_mines = sen.known_mines()
                new_safes = sen.known_safes()
                if new_mines:
                    self.mines |= new_mines
                    mines_safes_changed = True
                if new_safes:
                    self.safes |= new_safes
                    mines_safes_changed = True
                if new_mines or new_safes:
                    # Remove this sentence as the information has been processed
                    self.knowledge.remove(sen)

            # Update sentences with the known safe cells and known mines
            kb_changed = False
            if mines_safes_changed:
                for sen in self.knowledge:
                    for mine in self.mines:
                        if mine in sen.cells:
                            sen.cells.remove(mine)
                            sen.count -= 1
                            kb_changed = True
                    for safe_cell in self.safes:
                        if safe_cell in sen.cells:
                            sen.cells.remove(safe_cell)
                            kb_changed = True

            if kb_changed:
                update_knowledge()
            else:
                # Inferring new knowledge
                sen_changed = True
                kb_changed = False
                while sen_changed:
                    sen_changed = False
                    for i, j in itertools.combinations(range(len(self.knowledge)), 2):
                        s_i = self.knowledge[i]
                        s_j = self.knowledge[j]

                        if s_j.cells.issubset(s_i.cells):
                            s_i.cells -= s_j.cells
                            s_i.count -= s_j.count
                            sentence_changed = True
                            kb_changed = True
                        elif s_i.cells.issubset(s_j.cells):
                            s_j.cells -= s_i.cells
                            s_j.count -= s_i.count
                            sen_changed = True
                            kb_changed = True
                if kb_changed:
                    update_knowledge()

        update_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        move_list = list(self.safes - self.moves_made)
        move_nums = len(move_list)

        if move_nums > 0:
            new_move = random.choice(move_list)
            self.moves_made.add(new_move)
            return new_move
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        repeat = self.height * self.width - len(self.moves_made) - len(self.mines)

        while repeat > 0:
            new_move = (random.randrange(self.height),
                        random.randrange(self.width))
            if ((new_move not in self.moves_made) and (new_move not in self.mines)):
                self.moves_made.add(new_move)
                return new_move
            repeat -= 1

        return None
