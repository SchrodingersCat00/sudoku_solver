from pprint import pprint
import math
import copy

def solve(sudoku):
    queue = init_queue(sudoku)
    nuke(sudoku, queue)
    while not_solved(sudoku):
        prev = copy.deepcopy(sudoku)
        juuners_trick(sudoku, queue)
        other_trick(sudoku, queue)
        eliminate_singletons(sudoku, queue)
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
    square_len = int(math.sqrt(n))
    for coords in get_row_col_coords(n, n):
        yield coords
    square_coords = [k*square_len for k in range(square_len)]
    for i in square_coords:
        for j in square_coords:
            yield square_indices(i, j, n)

def get_row_col_coords(size, length, base_i=0, base_j=0, start_i=0, start_j=0):
    for n in range(size):
        yield [(base_i + n, start_j + dj) for dj in range(length)] # rows
        yield [(start_i + di, base_j + n) for di in range(length)] # columns

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

def other_trick(sudoku, queue): # fixen dat het niet enkel werkt voor squarelength
    square_len = int(math.sqrt(len(sudoku)))
    square_coords = [k*square_len for k in range(square_len)]
    for i in square_coords:
        for j in square_coords:
            counts = count_in_squares(sudoku, i, j)
            for check_coords, nuke_coords in zip(
                    get_row_col_coords(square_len, square_len, i, j, i, j), 
                    get_row_col_coords(square_len, len(sudoku), i, j)):
                nuke_all_singles(sudoku, check_coords, nuke_coords, counts, queue)

def nuke_all_singles(sudoku, check_coords, nuke_coords, counts, queue):
    square_size = int(math.sqrt(len(sudoku)))
    i, j = check_coords[0]
    for n in sudoku[i][j]:
        count = 0
        di, dj = check_coords[count]
        while count < len(check_coords) - 1 and n in sudoku[di][dj]:
            count += 1
            di, dj = check_coords[count]
        if n in sudoku[di][dj] and count + 1 == counts[n]:
            # pprint.pprint(sudoku, width=150)
            # print("n:", n)
            # print("count:", count)
            # print(check_coords)
            # print(nuke_coords)
            # pprint.pprint(counts)
            # print()
            nuke_at_coords(sudoku, n, nuke_coords, set(check_coords), queue)
                
def count_in_squares(sudoku, i, j):
    counts = {k:0 for k in range(1, len(sudoku)+1)}
    for si, sj in square_indices(i, j, len(sudoku)):
        for option in sudoku[si][sj]:
            counts[option] += 1
    return counts

def not_solved(sudoku):
    return any(any(len(item) > 1 for item in row) for row in sudoku)

def nuke(sudoku, queue):
    while queue:
        k, i, j = queue.pop()
        nuke_at_coords(sudoku, k, square_indices(i, j, len(sudoku)), {(i, j)}, queue)
        nuke_at_coords(sudoku, k, [(i, dj) for dj in range(len(sudoku))], {(i, j)} , queue)
        nuke_at_coords(sudoku, k, [(di, j) for di in range(len(sudoku))], {(i, j)}, queue)

def find_singletons(sudoku, coords):
    good = {i+1 for i in range(len(sudoku))}
    seen = set()
    for i, j in coords:
        for option in sudoku[i][j]:
            if option in seen:
                remove_from_el(good, option)
            seen.add(option)
    return [(k, i, j) for k in good for i, j in coords if k in sudoku[i][j] and len(sudoku[i][j]) > 1]

def eliminate_singletons(sudoku, queue):
    for coords in get_trick_coords(len(sudoku)):
        singletons = find_singletons(sudoku, coords)
        for number, i, j in find_singletons(sudoku, coords):
            sudoku[i][j] = {number}
            queue.add((number, i, j))

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
    pprint(sudoku)

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
    pprint(medium)

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
    pprint(hard)

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
    pprint(another, width=200)

    juuner = [[8,0,0,0,0,7,0,0,0],[2,0,0,0,0,8,6,0,9],[3,0,0,0,9,0,0,0,0],[0,9,0,2,5,0,0,0,0],[0,0,4,0,0,0,5,0,0],
     [0,0,0,0,6,4,0,3,0],[0,0,0,0,8,0,0,0,6],[7,0,2,1,0,0,0,0,5],[0,0,0,5,0,0,0,0,1]]
    
    for i in range(len(juuner)):
        for j in range(len(juuner)):
            if juuner[i][j] == 0:
                juuner[i][j] = None
    
    parsed = parse_sudoku(juuner)
    solve(parsed)
    pprint(parsed, width=200)

if __name__ == "__main__":
    main()