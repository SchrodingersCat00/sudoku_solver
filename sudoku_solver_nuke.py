import pprint
import math
import copy

def solve(sudoku):
    queue = init_queue(sudoku)
    nuke(sudoku, queue)
    while not_solved(sudoku):
        prev = copy.deepcopy(sudoku)
        juuners_trick(sudoku, queue)
        nuke(sudoku, queue)
        if prev == sudoku:
            print("This sudoku can not be solved")
            break

def juuners_trick(sudoku, queue):
    for coords in get_trick_coords(len(sudoku)):
        duplicates = find_duplicates(sudoku, coords)
        if duplicates:
            for duplicate in duplicates:
                i, j = duplicate[0]
                if len(duplicate) == len(sudoku[i][j]):
                    for ci, cj in duplicate:
                        options = sudoku[ci][cj]
                        for option in options:
                            nuke_at_coords(sudoku, option, coords, set(duplicate), queue)
                    break

def get_trick_coords(n):
    coords = []
    square_len = int(math.sqrt(n))
    for i in range(n):
        coords.append([(i, dj) for dj in range(n)])
        coords.append([(di, i) for di in range(n)])
    square_coords = [k*square_len for k in range(square_len)]
    for i in square_coords:
        for j in square_coords:
            coords.append(square_indices(i, j, n))
    return coords

def find_duplicates(sudoku, coords):
    duplicates = []
    for i in range(len(coords)):
        ci, cj = coords[i]
        current = [(ci, cj)]
        for j in range(i + 1, len(coords)):
            ki, kj = coords[j]
            if sudoku[ci][cj] == sudoku[ki][kj] and len(sudoku[ci][cj]) > 1:
                current.append((ki, kj))
        if len(current) > 1:
            duplicates.append(current)
    return duplicates


def not_solved(sudoku):
    return any(any(len(item) > 1 for item in row) for row in sudoku)

def nuke(sudoku, queue):
    while queue:
        k, i, j = queue.pop()
        nuke_at_coords(sudoku, k, square_indices(i, j, len(sudoku)), {(i, j)}, queue)
        nuke_at_coords(sudoku, k, [(i, dj) for dj in range(len(sudoku))], {(i, j)} , queue)
        nuke_at_coords(sudoku, k, [(di, j) for di in range(len(sudoku))], {(i, j)}, queue)

def nuke_at_coords(sudoku, k, coords, exceptset, queue):
    for i, j in coords:
        if (i, j) not in exceptset:
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
         [ None, None, None, None, 8, None, None, 7, 9]])
    
    solve(sudoku)
    pprint.pprint(sudoku)

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
    solve(medium)
    pprint.pprint(medium)

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

    solve(hard)
    pprint.pprint(hard)

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

    solve(another)
    pprint.pprint(another)

if __name__ == "__main__":
    main()