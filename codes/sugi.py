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

def brute_force_solve(grid, nodes_explored):
    return backtrack_brute(grid, nodes_explored)
    
def backtrack_brute(grid, nodes_explored):
    nodes_explored += 1   # CHANGE by JACEK
    row, col = find_unassigned_cell(grid)
    if row is None:
        return (True, nodes_explored) # Puzzle is solved | CHANGE by JACEK
    for num in range(1, 10):
        num = str(num)
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            (success, nodes_explored) = backtrack_brute(grid, nodes_explored)
            if (success == True):
                return (True, nodes_explored) # CHANGE by JACEK
            grid[row][col] = 'X'  # Backtrack
    return (False, nodes_explored)  # CHANGE by JACEK



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
def forward_checking_mrv(grid):
    def mrv_heuristic():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 'X':
                    return row, col, range(1, 10)
        return None, None, None  # No unassigned cells left

    def backtrack():
        nonlocal nodes_explored  # Declare nonlocal here
        row, col, domain = mrv_heuristic()
        if row is None:
            return True  # Puzzle is solved
        for num in domain:
            num = str(num)
            if is_valid_move(grid, row, col, num):
                grid[row][col] = num
                nodes_explored += 1  # Increment nodes_explored
                if backtrack():
                    return True
                grid[row][col] = 'X'  # Backtrack
        return False

    nodes_explored = 0  # Initialize nodes_explored

    if backtrack():
        return nodes_explored
    else:
        return 0

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

    input_file_path = filename # os.path.join(input_folder, filename)

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
            # Reset nodes_explored before each solving method
            global nodes_explored
            nodes_explored = 0

            # Solve the puzzle
            time_start = timeit.default_timer()
            if mode == "1":
                (solved, total_nodes) = brute_force_solve(grid, 0) # CHANGE by JACEK
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
                with open(input_file_path, 'r') as file:
                    for line in file:
                        print(line.strip())
                print("\nNumber of search tree nodes generated:", total_nodes)
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