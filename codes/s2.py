import csv
import time
import os,sys

# Define the Sudoku puzzle size (9x9 grid)
GRID_SIZE = 9

# Define input and output folder paths
input_folder = "C:\\Users\\sugip\\OneDrive\\Desktop\\IIT\\Intro to AI\\programming assignment 2\\testcase"
output_folder = "C:\\Users\\sugip\\OneDrive\\Desktop\\IIT\\Intro to AI\\programming assignment 2\\testcase_solution"

# Function to print the Sudoku grid
def print_grid(grid):
    for row in grid:
        print(','.join(map(str, row)))

# Function to check if a number is valid in a given row
def is_valid_in_row(grid, row, num):
    return num not in grid[row]

# Function to check if a number is valid in a given column
def is_valid_in_column(grid, col, num):
    return num not in [grid[row][col] for row in range(GRID_SIZE)]

# Function to check if a number is valid in a given 3x3 subgrid
def is_valid_in_subgrid(grid, row, col, num):
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
        is_valid_in_row(grid, row, num) and
        is_valid_in_column(grid, col, num) and
        is_valid_in_subgrid(grid, row, col, num)
    )

# Function to find the next unassigned cell
def find_unassigned_cell(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 'X':
                return row, col
    return None, None

# Brute Force Algorithm
def brute_force_solve(grid):
    row, col = find_unassigned_cell(grid)
    if row is None:
        return True  # Puzzle is solved
    for num in range(1, 10):
        num = str(num)
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if brute_force_solve(grid):
                return True
            grid[row][col] = 'X'  # Backtrack
    return False

# Backtracking Algorithm
def backtracking_solve(grid):
    row, col = find_unassigned_cell(grid)
    if row is None:
        return True  # Puzzle is solved
    for num in range(1, 10):
        num = str(num)
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if backtracking_solve(grid):
                return True
            grid[row][col] = 'X'  # Backtrack
    return False

# Forward Checking Algorithm with MRV heuristic
def forward_checking_mrv_solve(grid):
    def get_unassigned_cells(grid):
        unassigned_cells = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 'X':
                    unassigned_cells.append((row, col))
        return unassigned_cells

    def get_valid_moves(row, col):
        valid_moves = []
        for num in range(1, 10):
            num = str(num)
            if is_valid_move(grid, row, col, num):
                valid_moves.append(num)
        return valid_moves

    def mrv_heuristic(unassigned_cells):
        return min(unassigned_cells, key=lambda cell: len(get_valid_moves(cell[0], cell[1])))

    def forward_check(row, col):
        valid_moves = get_valid_moves(row, col)
        for move in valid_moves:
            grid[row][col] = move
            if forward_checking_mrv_solve(grid):
                return True
            grid[row][col] = 'X'  # Backtrack
        return False

    unassigned_cells = get_unassigned_cells(grid)
    if not unassigned_cells:
        return True  # Puzzle is solved
    row, col = mrv_heuristic(unassigned_cells)
    return forward_check(row, col)

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
    input_file_path = os.path.join(input_folder, filename)
    
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
        with open(input_file_path, 'r') as file:
            reader = csv.reader(file)
            grid = [row for row in reader]

        if mode in ("1", "2", "3"):
            # Solve the puzzle
            start_time = time.time()
            if mode == "1":
                solved = brute_force_solve(grid)
            elif mode == "2":
                solved = backtracking_solve(grid)
            elif mode == "3":
                solved = forward_checking_mrv_solve(grid)
            search_time = time.time() - start_time
            if not solved:
                print("No solution found.")
            else:
                print(f"Last Name, First Name, AXXXXXXXX solution:")
                print(f"Input file: {filename}")
                print(f"Algorithm: {algorithm_name}")
                print("\nInput puzzle:")
                print_grid(grid)
                print("\nNumber of search tree nodes generated:", 0)  # Not implemented
                print("Search time:", search_time, "seconds")
                print("\nSolved puzzle:")
                print_grid(grid)
                # Validate and save the solution
                if is_valid_solution(grid):
                    solution_filename = filename.replace(".csv", "_SOLUTION.csv")
                    # Modify the solution_file_path to include the output folder
                    solution_file_path = os.path.join(output_folder, solution_filename)
                    with open(solution_file_path, 'w', newline='') as solution_file:
                        writer = csv.writer(solution_file)
                        writer.writerows(grid)
                    print(f"\nSolution saved to {solution_file_path}")
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
