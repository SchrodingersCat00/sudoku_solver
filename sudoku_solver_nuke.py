import pprint
import math

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
         [ None, None, None, None, 8, None, None, 7, 9]])
    
    nuke(sudoku)
    pprint.pprint(sudoku)

if __name__ == "__main__":
    main()