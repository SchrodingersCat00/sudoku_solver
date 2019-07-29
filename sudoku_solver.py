import math
import pprint
import copy

PRINT_DEBUG = True

# Solves the sudoku and returns a boolean
def solve(sudoku):
    global PRINT_DEBUG
    nuked = nuke(sudoku)
    print("---- NUKED SUDOKU ----")
    pprint.pprint(nuked)
    print("---- CONTAINS EMPTY-----")
    print(contains_empty(nuked))
    if contains_empty(nuked):
        return False
    print("------NOT SOLVED-----")
    print(not_solved(nuked))
    if not not_solved(nuked):
        return True
    print("-----UNSOLVED POSITIONS------")
    print(unsolved_positions(nuked))
    for i, j  in unsolved_positions(nuked):
        print("-----CURRENT POSITION-----")
        pprint.pprint((i, j))
        print()
        temp = nuked[i][j]
        for possibilitiy in nuked[i][j]:
            print("---- CURRENT POSSIBILTY-----")
            print(possibilitiy)
            nuked[i][j] = {possibilitiy}
            print("----SUDOKU WITH POSSIBILITY----")
            pprint.pprint(nuked)
            # remove all possibilities except possibility
            if solve(nuked):
                return True
            # add possibilies back
        nuked[i][j] = temp
        print("-----SUDOKU AFTER POSSIBILITY----")
        pprint.pprint(nuked)
        return False
    return False

def contains_empty(sudoku):
    return any(any(len(item) == 0 for item in row) for row in sudoku)

# Returns a sorted list of unsolved positions, 
def unsolved_positions(sudoku):
    n = len(sudoku)
    return [(i, j) for i in range(n) for j in range(n) if len(sudoku[i][j]) > 1]

def not_solved(sudoku):
    return any(any(len(item) > 1 for item in row) for row in sudoku)

def nuke(input_sudoku):
    sudoku = copy.deepcopy(input_sudoku)
    queue = init_queue(sudoku)
    while queue:
        k, i, j = queue.pop()
        nuke_at_coords(sudoku, k, square_indices(i, j, len(sudoku)), queue)
        nuke_at_coords(sudoku, k, [(i, dj) for dj in range(len(sudoku))], queue)
        nuke_at_coords(sudoku, k, [(di, j) for di in range(len(sudoku))], queue)
        sudoku[i][j] = {k}
    return sudoku

def nuke_at_coords(sudoku, k, coords, queue):
    for i, j in coords:
        if remove_from_el(sudoku[i][j], k):
            add_to_queue(sudoku, i, j, queue)

def remove_from_el(el, k):
    try:
        el.remove(k)
        return True
    except (KeyError):
        return False

def square_indices(i, j, n):
    square_size = int(math.sqrt(n))
    base_i = i - (i%square_size)
    base_j = j - (j%square_size)
    indices = []
    for di in range(square_size):
        for dj in range(square_size):
            indices.append((base_i + di, base_j + dj))
    return indices

def add_to_queue(sudoku, i, j, queue):
    if len(sudoku[i][j]) == 1:
        for item in sudoku[i][j]:
            k = item
        queue.add((k, i, j))

def init_queue(sudoku):
    queue = set()
    n = len(sudoku)
    for i in range(n):
        for j in range(n):
            add_to_queue(sudoku, i, j, queue)
    return queue

def parse_sudoku(sudoku_list):
    def parse_item(item):
        if item is None:
            return {i+1 for i in range(len(sudoku_list))}
        else:
            return {item}
    return [[parse_item(item) for item in row] for row in sudoku_list]

def main():
    sudoku = parse_sudoku(
        [[ 5, 3, None, None, 7, None, None, None, None],
         [ 6, None, None, 1, 9, 5, None, None, None],
         [ None, 9, 8, None, None, None, None, 6, None ],
         [ 8, None, None, None, 6, None, None, None, 3 ],
         [ 4, None, None, 8, None, 3, None, None, 1 ],
         [ 7, None, None, None, 2, None, None, None, 6],
         [ None, 6, None, None, None, None, 2, 8, None],
         [ None, None, None, 4, 1, 9, None, None, 5],
         [ None, None, None, None, 8, None, None, 7, 9]]
    )
    hard = parse_sudoku(
        [[None, None, None, None, None, None, 4, None, None],
        [4, None, None, None, 3, 2, None, 5, 1],
        [None, 5, 2, 6, 4, None, None, None, 3],
        [None, 2, None, None, None, None, 5, None, None],
        [None, None, None, 4, None, 3, None, None, None],
        [None, None, 7, None, None, None, None, 3, None],
        [6, None, None, None, 1, 4, 7, 9, None],
        [7, 8, None, 2, 9, None, None, None, 6],
        [None, None, 1, None, None, None, None, None, None]]
    )
    medium = parse_sudoku(
        [[6, None, None, 8, 1, 4, 9, None, None],
        [5, None, None, 6, 9, None, None, 1, None],
        [1, None, None, None, None, 3, None, None, None],
        [None, 1, None, None, None, None, 6, 4, None],
        [None, 5, None, None, None, None, None, 3, None],
        [None, 7, 6, None, None, None, None, 9, None],
        [None, None, None, 4, None, None, None, None, 9],
        [None, 9, None, None, 5, 1, None, None, 3],
        [None, None, 1, 3, 7, 9, None, None, 5]]
    )

    another = parse_sudoku(
        [[None, None, None, None, None, None, 2, None, None],
        [None, 8, None, None, None, 7, None, 9, None, ],
        [6, None, 2, None, None, None, 5, None, None],
        [None, 7, None, None, 6, None, None, None, None],
        [None, None, None, 9, None, 1, None, None, None],
        [None, None, None, None, 2, None, None, 4, None],
        [None, None, 5, None, None, None, 6, None, 3],
        [None, 9, None, 4, None, None, None, 7, None],
        [None, None, 6, None, None, None, None, None, None]]
    )
    
    another_solution = [
        [9, 5, 7, 6, 1, 3, 2, 8, 4],
        [4, 8, 3, 2, 5, 7, 1, 9, 6],
        [6, 1, 2, 8, 4, 9, 5, 3, 7],
        [1, 7, 8, 3, 6, 4, 9, 5, 2],
        [5, 2, 4, 9, 7, 1, 3, 6, 8],
        [3, 6, 9, 5, 2, 8, 7, 4, 1],
        [8, 4, 5, 7, 9, 2, 6, 1, 3],
        [2, 9, 1, 4, 3, 6, 8, 7, 5],
        [7, 3, 6, 1, 8, 5, 4, 2, 9]
    ]
    # pprint.pprint(solve(hard))
    # pprint.pprint(sudoku)
    # pprint.pprint(hard)
    
    # solve(another)
    # pprint.pprint(another)
    print(solve(sudoku))
    

if __name__ == '__main__':
    main()