import math
import pprint

PRINT_DEBUG = True

# Solves the sudoku and returns a boolean
def solve(sudoku):
    global PRINT_DEBUG
    nuke(sudoku)
    if PRINT_DEBUG:
        pprint.pprint(sudoku)
        PRINT_DEBUG = False
    # print("---- NUKED SUDOKU ----")
    # pprint.pprint(sudoku)
    # print("---- CONTAINS EMPTY-----")
    # print(contains_empty(sudoku))
    if contains_empty(sudoku):
        return False
    # print("------NOT SOLVED-----")
    # print(not_solved(sudoku))
    if not not_solved(sudoku):
        print("ok")
        return True
    # print("-----UNSOLVED POSITIONS------")
    # print(unsolved_positions(sudoku))
    for i, j  in unsolved_positions(sudoku):
        # print("-----CURRENT POSITION-----")
        # pprint.pprint((i, j))
        # print()
        temp = sudoku[i][j]
        for possibilitiy in sudoku[i][j]:
            # print("---- CURRENT POSSIBILTY-----")
            # print(possibilitiy)
            sudoku[i][j] = {possibilitiy}
            # print("----SUDOKU WITH POSSIBILITY----")
            # pprint.pprint(sudoku)
            # remove all possibilities except possibility
            if solve(sudoku):
                return True
            # add possibilies back
            sudoku[i][j] = temp
            # print("-----SUDOKU AFTER POSSIBILITY----")
            # pprint.pprint(sudoku)
    return False

def contains_empty(sudoku):
    return any(any(len(item) == 0 for item in row) for row in sudoku)

# Returns a sorted list of unsolved positions, 
def unsolved_positions(sudoku):
    n = len(sudoku)
    return [(i, j) for i in range(n) for j in range(n) if len(sudoku[i][j]) > 1]

def not_solved(sudoku):
    return any(any(len(item) > 1 for item in row) for row in sudoku)

def nuke(sudoku):
    queue = init_queue(sudoku)
    while queue:
        k, i, j = queue.pop()
        nuke_at_coords(sudoku, k, square_indices(i, j, len(sudoku)), queue)
        nuke_at_coords(sudoku, k, [(i, dj) for dj in range(len(sudoku))], queue)
        nuke_at_coords(sudoku, k, [(di, j) for di in range(len(sudoku))], queue)
        sudoku[i][j] = {k}

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
    
    # solve(sudoku)
    # pprint.pprint(solve(hard))
    # pprint.pprint(sudoku)
    # pprint.pprint(hard)
    solve(another)
    pprint.pprint(another)

if __name__ == '__main__':
    main()