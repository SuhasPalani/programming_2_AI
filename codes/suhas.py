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

# Function Brute-Force
def brute_force_solve(board, index, total_nodes, max_nodes):
    if index == 81:
        # Complete assignment reached, check if it is consistent
        if is_consistent(board):
            return (True, total_nodes + 1)
        return (False, total_nodes + 1)

    if total_nodes > max_nodes:
        return (False, total_nodes)

    row, col = divmod(index, 9)

    # Skip over cells with known values
    if board[row][col] != 'X':
        return brute_force_solve(board, index + 1, total_nodes + 1, max_nodes)

    for num in range(1, 10):
        # Assign value and explore the next variable
        board[row][col] = str(num)
        (solved, total_nodes) = brute_force_solve(board, index + 1, total_nodes + 1, max_nodes)

        if solved:
            return (True, total_nodes)

    # If no value leads to a solution, backtrack
    board[row][col] = 'X'
    return (False, total_nodes)

# Backtracking Algorithm
def backtracking_solve(grid):
    global nodes_explored

    def backtrack():
        global nodes_explored  # Reference the global variable
        row, col = find_unassigned_cell(grid)
        if row is None:
            return True  # Puzzle is solved
        for num in range(1, 10):
            num = str(num)
            if is_valid_move(grid, row, col, num):
                grid[row][col] = num
                nodes_explored += 1  # Increment nodes_explored
                if backtrack():
                    return True
                grid[row][col] = 'X'  # Backtrack
        return False

    nodes_explored = 0
    return backtrack()

# Forward Checking Algorithm with MRV heuristic (modified)
def forward_checking_mrv(board, max_nodes):
    def mrv_heuristic():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 'X':
                    return row, col, range(1, 10)
        return None, None, None  # No unassigned cells left

    def backtrack():
        nonlocal total_nodes  # Use nonlocal here
        row, col, domain = mrv_heuristic()
        if row is None:
            return True  # Puzzle is solved
        for num in domain:
            num = str(num)
            if is_valid_move(board, row, col, num):
                board[row][col] = num
                total_nodes[0] += 1  # Increment total_nodes
                if total_nodes[0] > max_nodes:
                    return False  # Stop if the limit is reached
                if backtrack():
                    return True
                board[row][col] = 'X'  # Backtrack
        return False

    total_nodes = [0]  # Initialize total_nodes as a list

    if backtrack():
        return total_nodes[0]  # Return total_nodes when the puzzle is solved
    else:
        return 0  # Return 0 when the puzzle is not solved


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

# Main function
def main():
    if len(sys.argv) != 3:
        print("ERROR: Not enough/too many input arguments.")
        return

    mode = sys.argv[1]
    filename = sys.argv[2]

    input_file_path = filename  # os.path.join(input_folder, filename)

    grid = None  # Initialize grid variable

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
        # Read the Sudoku puzzle from the input file
        grid = read_sudoku_from_csv(input_file_path)

        if mode in ("1", "2", "3"):
            # Solve the puzzle
            time_start = timeit.default_timer()
            if mode == "1":
                # Initialize nodes_explored for Brute Force
                # nodes_explored = 0
                max_nodes = 1000  # Set your desired limit
                (solved, total_nodes) = brute_force_solve(copy.deepcopy(grid), 0, 0, max_nodes)
                print("Number of search tree nodes generated:", total_nodes)
            elif mode == "2":
                solved = backtracking_solve(grid)
            elif mode == "3":
                solved = forward_checking_mrv(grid)
            search_time = timeit.default_timer() - time_start

            if not solved:
                print("No solution found.")
            else:
                print(f"Last Name, First Name, AXXXXXXXX solution:")
                print(f"Input file: {filename}")
                print(f"Algorithm: {algorithm_name}")
                print("\nInput puzzle:")
                # Display the input puzzle as per the contents from the CSV file
                grid_print(grid)
                print("\nNumber of search tree nodes generated:", nodes_explored)
                print("Search time: {:.3f} seconds".format(round(search_time, 3)))
                print("\nSolved puzzle:")
                if is_valid_solution(grid):
                    grid_print(grid)
                    # Save the solution to the output folder
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
            # Validate the puzzle
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
