import csv
import timeit
import os
import sys
import copy

# Defining the Sudoku puzzle size
GRID_SIZE = 9

# Defining input and output folder paths
input_folder = "C:\\Users\\sugip\\OneDrive\\Desktop\\IIT\\Intro to AI\\programming assignment 2\\testcase"
output_folder = "C:\\Users\\sugip\\OneDrive\\Desktop\\IIT\\Intro to AI\\programming assignment 2\\testcase_solution\\mode_{mode}"

# The implementation of a global variable to track the number of nodes in a search tree.
nodes_explored = 0

# Function to print the Sudoku grid
def grid_print(grid):
    for row in grid:
        print(','.join(map(str, row)))

# Function to check if a number is valid in a given row
def is_valid_row(grid, row, num):
    return num not in grid[row]

# Function to check if a number is valid in a given column
def is_valid_column(grid, col, num):
    return num not in [grid[row][col] for row in range(GRID_SIZE)]

# Function to check if a number is valid in a given 3x3 subgrid
def is_valid_subgrid(grid, row, col, num):
    subgrid_row = row // 3
    subgrid_col = col // 3
    for i in range(subgrid_row * 3, (subgrid_row + 1) * 3):
        for j in range(subgrid_col * 3, (subgrid_col + 1) * 3):
            if grid[i][j] == num:
                return False
    return True

# Function to check if a number is valid in a given cell
def is_valid_move(grid, row, col, num):
    return (
        is_valid_row(grid, row, num) and
        is_valid_column(grid, col, num) and
        is_valid_subgrid(grid, row, col, num)
    )

# Function to find the next unassigned cell
def find_unassigned_cell(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 'X':
                return row, col
    return None, None

# Function to read Sudoku puzzle from CSV file
def read_sudoku_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def brute_force_solve(board, max_nodes):
    global nodes_explored
    nodes_explored += 1

    if nodes_explored > max_nodes:
        return False, nodes_explored

    empty_cell = find_unassigned_cell(board)
    if empty_cell == (None, None):
        # All cells are filled, check if the assignment is consistent
        return is_consistent(board), nodes_explored

    row, col = empty_cell

    for num in range(1, 10):
        # Assign value and explore the next variable
        board[row][col] = str(num)
        solved, total_nodes = brute_force_solve(board, max_nodes)
        if solved:
            return True, total_nodes

    # If no value leads to a solution, backtrack
    board[row][col] = 'X'
    return False, nodes_explored



def mrv_heuristic(grid):
    empty_cells = [(row, col, get_possible_values(grid, row, col)) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == 'X']
    
    if not empty_cells:
        return None, None, None  # No unassigned cells left
    
    # Select the cell with the minimum remaining values (MRV)
    min_cell = min(empty_cells, key=lambda cell: len(cell[2]))
    return min_cell[0], min_cell[1], min_cell[2]

def brute_force_main(grid):
    global nodes_explored
    nodes_explored = 0  # Initialize nodes_explored
    if brute_force_solve(grid):
        return nodes_explored
    else:
        return 0

# Backtracking Algorithm
def backtracking_solve(grid):
    global nodes_explored

    def backtrack(row, col, nodes_explored):
        if row is None:
            return True, nodes_explored  # Puzzle is solved

        for num in range(1, 10):
            num = str(num)
            if is_valid_move(grid, row, col, num):
                grid[row][col] = num
                nodes_explored += 1  # Increment nodes_explored
                next_row, next_col = find_unassigned_cell(grid)
                solved, nodes_explored = backtrack(next_row, next_col, nodes_explored)
                if solved:
                    return True, nodes_explored
                grid[row][col] = 'X'  # Backtrack

        return False, nodes_explored

    initial_row, initial_col = find_unassigned_cell(grid)
    nodes_explored = 0
    return backtrack(initial_row, initial_col, nodes_explored)


# Forward Checking Algorithm with MRV heuristic (modified)
def forward_checking_mrv(board, max_nodes):
    def mrv_heuristic():
        empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if board[row][col] == 'X']
        if not empty_cells:
            return None, None, None  # No unassigned cells left

        # Select the cell with the minimum remaining values (MRV)
        min_cell = min(empty_cells, key=lambda cell: len(get_possible_values(board, cell[0], cell[1])))
        return min_cell[0], min_cell[1], get_possible_values(board, min_cell[0], min_cell[1])

    def backtrack():
        nonlocal nodes_explored  # Declare nonlocal here
        row, col, domain = mrv_heuristic()
        if row is None:
            return True  # Puzzle is solved
        for num in domain:
            num = str(num)
            if is_valid_move(board, row, col, num):
                board[row][col] = num
                nodes_explored += 1  # Increment nodes_explored
                if nodes_explored > max_nodes:
                    return False  # Stop if the limit is reached
                if backtrack():
                    return True
                board[row][col] = 'X'  # Backtrack
        return False

    nodes_explored = 0  # Initialize nodes_explored

    if backtrack():
        return nodes_explored
    else:
        return 0
    
    
    
def is_consistent(board):
    for row in board:
        if len(set(row)) != len(row):
            return False

    for col in range(GRID_SIZE):
        if len(set(board[row][col] for row in range(GRID_SIZE))) != GRID_SIZE:
            return False

    for subgrid_row in range(0, GRID_SIZE, 3):
        for subgrid_col in range(0, GRID_SIZE, 3):
            subgrid = [
                board[row][col]
                for row in range(subgrid_row, subgrid_row + 3)
                for col in range(subgrid_col, subgrid_col + 3)
            ]
            if len(set(subgrid)) != GRID_SIZE:
                return False

    return True

# Function to validate the solved puzzle
def is_valid_solution(grid):
    for row in grid:
        if sorted(row) != [str(num) for num in range(1, 10)]:
            return False
    for col in range(GRID_SIZE):
        if sorted([grid[row][col] for row in range(GRID_SIZE)]) != [str(num) for num in range(1, 10)]:
            return False
    for subgrid_row in range(0, GRID_SIZE, 3):
        for subgrid_col in range(0, GRID_SIZE, 3):
            subgrid = [grid[row][col] for row in range(subgrid_row, subgrid_row + 3) for col in range(subgrid_col, subgrid_col + 3)]
            if sorted(subgrid) != [str(num) for num in range(1, 10)]:
                return False
    return True

# Function to get possible values for a cell
def get_possible_values(grid, row, col):
    values = set(range(1, 10))
    # Check row
    values -= set(grid[row])
    # Check column
    values -= set(grid[i][col] for i in range(GRID_SIZE))
    # Check box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    values -= set(grid[i][j] for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3))
    return list(values)


# Main function
def main():
    if len(sys.argv) != 3:
        print("ERROR: Not enough/too many input arguments.")
        return

    mode = sys.argv[1]
    filename = sys.argv[2]

    input_file_path = filename

    grid = None

    if mode == "1":
        algorithm_name = "Brute Force"
    elif mode == "2":
        algorithm_name = "Backtracking"
    elif mode == "3":
        algorithm_name = "Forward Checking with MRV"
    elif mode == "4":
        algorithm_name = "Test"
    else:
        print("ERROR: Invalid mode.")
        return

    try:
        grid = read_sudoku_from_csv(input_file_path)
        if mode in ("1", "2", "3"):
            # Solve the puzzle
            time_start = timeit.default_timer()
            total_nodes = 0  
            if mode == "1":
                max_nodes = float('inf')
                (solved, total_nodes) = brute_force_solve(copy.deepcopy(grid), max_nodes)

                print("Number of search tree nodes generated:", total_nodes)
            elif mode == "2":
                solved, total_nodes = backtracking_solve(grid)
                print("Number of search tree nodes generated:", total_nodes)
            elif mode == "3":
                time_start = timeit.default_timer()
                total_nodes = forward_checking_mrv(grid, float('inf'))
                solved = total_nodes > 0

            time_end = timeit.default_timer()
            search_time = time_end - time_start

            if not solved:
                print("No solution found.")
            else:
                print(f"\nPalani, Suhas, A20548277 solution:")
                print(f"Input file: {filename}")
                print(f"Algorithm: {algorithm_name}")
                print("\nInput puzzle:")
                with open(input_file_path, 'r') as file:
                    for line in file:
                        print(line.strip())
                print("\nNumber of search tree nodes generated:", total_nodes)
                print("Search time: {:.4f} seconds".format(round(search_time, 4)))
                print("\nSolved puzzle:")
                if is_valid_solution(grid):
                    grid_print(grid)
                    if mode in ("1", "2", "3"):
                        solution_filename = filename.replace(".csv", f"_mode_{mode}_SOLUTION.csv")
                        solution_file_path = os.path.join(output_folder.format(mode=mode), solution_filename)
                        with open(solution_file_path, 'w', newline='') as solution_file:
                            writer = csv.writer(solution_file)
                            writer.writerows(grid)
                        print(f"\nSolution saved to testcase-> mode_{mode}")
                else:
                    print("ERROR: This is NOT a solved Sudoku puzzle.")
        elif mode == "4":
            if is_valid_solution(grid):
                print("This is a valid, solved, Sudoku puzzle.")
            else:
                print("ERROR: This is NOT a solved Sudoku puzzle.")
        else:
            print("ERROR: Invalid mode.")
    except FileNotFoundError:
        print(f"ERROR: Input file not found in {input_folder}")

if __name__ == "__main__":
    main()
