import os

# Misplaced tile heuristic.
    def misplaced_tiles(puzzle):

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