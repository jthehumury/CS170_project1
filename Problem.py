# Imports for math functions.
from math import sqrt
from math import floor

# Imports for GUI display (Windows).
import os

# ------------------------------------------------------------------------------------------
# NODE CLASS

class Node:

    # Declare initial vars for each node.
    def __init__(self, state, g, mode):
        self.state = state
        self.g = g
        self.h = 0
        self.mode = mode

    # Misplaced tile heuristic.
    def misplaced_tiles(self):

        # Count misplaced tiles.
        count = 0

        # Get dimensions of puzzle.
        size_of_game = len(self.state)

        # Define the goal state for 3 x 3.
        goal = [1,2,3,4,5,6,7,8,0]

        # Compare each tile to the goal state.
        for i in range(size_of_game):
            if goal[i] != self.state[i]:
                count += 1

        return count

    # Calculate search.
    def f(self):

        self.h = 0

        # Uniform cost search.
        if self.mode == 1:
            return self.g

        # Get dimensions of puzzle.
        size_of_game = len(self.state)
        dimensions = sqrt(size_of_game)

        # Iterate through each tile.
        for i in range(size_of_game):

            if self.state[i] == 0:
                continue

            # Determine displacement of tile relative to its goal position.
            horizontal_distance = (i % dimensions) - ((self.state[i] - 1) % dimensions)
            vertical_distance = floor(i / dimensions) - floor((self.state[i] - 1)/dimensions)

            # Calculate euclidean distance based on displacement.
            euclidean_distance = sqrt(horizontal_distance ** 2 + vertical_distance ** 2)

            # A* - Misplaced Tiles
            if self.mode == 2:
                self.h += self.misplaced_tiles()

            # A* - Euclidean Distance
            if self.mode == 3:
                self.h += euclidean_distance

        # f(n) = h(n) + g(n)
        return self.h + self.g

    # Display heuristics and current puzzle.
    def display(self):

        # Display heuristics results.
        dimensions=sqrt(len(self.state))
        print("-------------\n")
        print("f(n) = " + str(self.f()))
        print("g(n) = " + str(self.g))
        print("h(n) = " + str(self.h) + "\n")

        # Display vars.
        col_index = 0
        first_col = "0"
        second_col = "0"
        third_col = "0"

        # Iterate through the puzzled and display.
        for i in range(len(self.state)):

            # Drop to new line.
            if i % dimensions == 0:
                col_index = 0

            # Replace zero with blank.
            if self.state[i] == 0:
                if col_index == 0:
                    first_col = "*"
                if col_index == 1:
                    second_col = "*"
                if col_index == 2:
                    third_col = "*"

            # Otherwise, print tile.
            else:
                if col_index == 0:
                    first_col = str(self.state[i])
                if col_index == 1:
                    second_col = str(self.state[i])
                if col_index == 2:
                    third_col = str(self.state[i])

            # Print row and heuristics.
            if col_index == 2:
                print(first_col + " " + second_col + " " + third_col)
            else:
                col_index += 1

        # Newline.
        print("")

# ------------------------------------------------------------------------------------------
# PROBLEM CLASS

class Problem:

    # Match problem space definition.
    def __init__(self, start):
        self.start_state = start
        self.goal_state = [1,2,3,4,5,6,7,8,0]
        self.frontier = []
        self.max_q = 0
        self.explored = []

    # Perform search based on mode.
    def graph_search(self, mode):
        
        # Mode 1 - Uniform Cost Search
        node = Node(self.start_state, 0, 1)
        #node = Node(self.start_state, 0, mode)
        node.display()

        # Return if goal state is met.
        if node.state == self.goal_state:
            return node

        # Update node if not in goal state.
        self.update_frontier(node, mode)

        while (True):

            # Return on empty frontier.
            if not self.frontier:
                return None

            # Get min node, check if visited.
            current_state = self.remove_state()
            if current_state.state in self.explored:
                continue

            # Display current node.
            current_state.display()

            # Add node to list of explored nodes.
            self.explored.append(current_state.state)
            if current_state.state == self.goal_state:
                return current_state

            self.update_frontier(current_state, mode)

    # Update frontier based on current state.
    def update_frontier(self, current_state, mode):
        
        # Obtain puzzle metadata.
        size_of_game = len(current_state.state)
        g = current_state.g + 1
        dimensions = int(sqrt(size_of_game))
        i = None

        # Get location of the blank tile.
        for x in range(size_of_game):
            if current_state.state[x] == 0:
                i = x

        # Get coordinates of blank tile.
        x_coordinate = i % dimensions
        y_coordinate = floor(i / dimensions)

        # If tile not at left edge.
        if x_coordinate + 1 <= 2:

            # Swap blank tile with adjacent tile.
            new_state = list(current_state.state)
            new_state[i], new_state[i+1] = new_state[i+1], new_state[i]

            # Check if new state has already been explored.
            if self.check_frontier(new_state) and new_state not in self.explored:
                node = Node(new_state, g, mode)
                self.frontier.append(node)
        
        # If tile not at right edge.
        if x_coordinate - 1 >= 0:
            new_state=list(current_state.state)
            new_state[i], new_state[i-1] = new_state[i - 1], new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node = Node(new_state, g, mode)
                self.frontier.append(node)
        
        # If tile not at bottom edge.
        if y_coordinate + 1 <= 2:
            new_state = list(current_state.state)
            new_state[i], new_state[i + dimensions] = new_state[i + dimensions], new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node = Node(new_state, g, mode)
                self.frontier.append(node)
        
        # If tile not at top edge.
        if y_coordinate - 1 >= 0:
            new_state=list(current_state.state)
            new_state[i], new_state[i - dimensions] = new_state[i - dimensions], new_state[i]
            if self.check_frontier(new_state) and new_state not in self.explored:
                node = Node(new_state, g, mode)
                self.frontier.append(node)
        
        if len(self.frontier) > self.max_q:
            self.max_q = len(self.frontier)

    # Check if current state is in frontier.
    def check_frontier(self, check_state):

        # Iterate through frontier.
        for i in self.frontier:
            if i.state == check_state:
                return False

        return True

    # Remove min from frontier.
    def remove_state(self):

        # Determine lowest min value.
        min_f = None
        for i in self.frontier:

            if min_f:
                if i.f() < min_f.f():
                    min_f = i
            else:
                min_f = i

        # Remove min from frontier.
        self.frontier.remove(min_f)
        return min_f

# ------------------------------------------------------------------------------------------
# GUI FUNCTIONS

def intro():

    # Clear screen.
    os.system("cls")

    # Display contributors and project metadata.
    print("CS170 Project 01 - Eight Puzzle Solver")
    print("Completed 04/27/2021\n")
    print("Otniel Thehumury / otheh001 / 862029595")
    print("Matthew Walsh / mwals003 / 862088280\n")
    print("---------------------------------------\n")

    # Prompt user for choice of puzzle.
    print("Select from the following options:\n")
    print(" 1) Use default puzzle (LONG).       1 2 3")
    print(" 2) Enter your own puzzle.           4 5 6")
    print(" 3) Quick solution puzzle.           7 8 b\n")
    
    choice = int(input("Enter Choice Here: "))

    # Define new puzzle.
    puzzle = []
    SIZE = 9
    dimensions=sqrt(SIZE)

    # Allow user to enter their own puzzle.
    if choice == 2:
        for i in range(SIZE):
            x_coordinate = int(i % dimensions)
            y_coordinate = int(floor(i / dimensions))
            cell=input("Enter cell[" + str(y_coordinate) + "][" + str(x_coordinate) + "]: ")
            puzzle.append(cell)
    
    # Trillion-step "Oh Boy" puzzle.
    elif choice == 1:
        puzzle=[8,7,1,6,0,2,5,4,3]

    else:
        puzzle=[1,2,3,4,5,6,0,7,8]

    # Prompt the user to select a choice.
    print("\nPlease choose from the following algorithms:\n")
    print("1) Uniform Cost Search              1 2 3    1 2 3")
    print("2) A* - Misplace Tile Heurisitc     4 8 b -> 4 5 6")
    print("3) A* - Euclidean Dist Heuristic    7 6 5    7 8 b\n")

    mode = input("Enter Choice Here: ")
    
    print("")

    return (puzzle,mode)

# Display results of algorithm.
def display_results(result):
    print("-------------")
    if result:
        print("This solution took " + str(result.g) + " moves")
        print("The maximum size of the frontier is " + str(problem.max_q))
    else:
        print("There is no solution")

# ------------------------------------------------------------------------------------------
# MAIN FUNCTIONALITY

puzzle_mode_tuple = intro()
problem = Problem(puzzle_mode_tuple[0])
display_results(problem.graph_search(puzzle_mode_tuple[1]))