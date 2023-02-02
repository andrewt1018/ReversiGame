import numpy as np



class Reversi:
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self, size):
        assert (size % 2 == 0 and size > 2)
        self.size = size
        self.grid = [[Reversi.EMPTY for _ in range(size)] for _ in range(size)]  # [row][column]
        middle = int(self.size / 2)
        self.grid[middle][middle] = Reversi.BLACK
        self.grid[middle - 1][middle - 1] = Reversi.BLACK
        self.grid[middle][middle - 1] = Reversi.WHITE
        self.grid[middle - 1][middle] = Reversi.WHITE
        # the possible actions the next player / agent can make
        self.action_space = [(middle - 2, middle), (middle - 1, middle + 1), (middle, middle - 2),
                             (middle + 1, middle - 1)]

        # Black starts first
        self.white_move = False

    # update the grid and action space after the player make an action
    def step(self, action):
        grid = self.grid
        if action in self.action_space:
            x, y = action
            if (self.white_move):  # If white moves
                grid[x][y] = Reversi.WHITE
                grid = self.update_grid(grid, action)
                self.white_move = False
            else:
                grid[x][y] = Reversi.BLACK
                grid = self.update_grid(grid, action)
                self.white_move = True
        else:
            return -1

        action_space = self.update_action_space(grid)
        action_space = [*set(action_space)]
        self.grid = grid
        self.action_space = action_space
        # return next_state, reward, done
        return self.check_if_win(grid);

    # Checks whether the entire grid is filled, and returns the winner
    # Returns 0 if grid is not filled yet
    # Returns 1 if white wins
    # Returns 2 if black wins
    # Returns 3 if tie
    def check_if_win(self, grid):
        white_count = 0
        black_count = 0
        for x in range(self.size):
            for y in range(self.size):
                if grid[x][y] == 0:
                    return 0
                elif grid[x][y] == 1:
                    white_count += 1
                elif grid[x][y] == 2:
                    black_count += 1
        if white_count >= black_count:
            diff = white_count - black_count
            print(f"Congratulations to White for winning with {diff} more pieces than Black!")
            return 1
        elif black_count >= white_count:
            diff = black_count - white_count
            print(f"Congratulations to Black for winning with {diff} more pieces than White!")
            return 2
        else:
            print(f"Tie! Both players ended up with {black_count} pieces on the board.")
            return 3

    # Update the grid after a player makes a move. Converts any piece in between to the opposite color
    def update_grid(self, grid, action):
        x, y = action
        current_color = grid[x][y]
        for dir in range(8):
            if (dir == 0):  # check right
                ret = self._continued_check(grid, action, dir, current_color)
                if ret == 1:
                    gridy = y + 1
                    while gridy < self.size:
                        if (grid[x][gridy] == current_color):
                            break
                        grid[x][gridy] = current_color
                        gridy += 1
            if (dir == 1):  # check top right
                ret = self._continued_check(grid, action, dir, current_color)
                if (ret == 1):
                    gridx, gridy = x - 1, y + 1
                    while gridx > 0 and gridy < self.size:
                        if grid[gridx][gridy] == current_color:
                            break
                        grid[gridx][gridy] = current_color
                        gridx -= 1
                        gridy += 1
            if (dir == 2):  # check upwards
                ret = self._continued_check(grid, action, dir, current_color)
                if ret == 1:
                    gridx = x - 1
                    while gridx > 0:
                        if grid[gridx][y] == current_color:
                            break
                        grid[gridx][y] = current_color
                        gridx -= 1
            if dir == 3:  # check top left
                ret = self._continued_check(grid, action, dir, current_color)
                if (ret == 1):
                    gridx, gridy = x - 1, y - 1
                    while gridx > 0 and gridy > 0:
                        if grid[gridx][gridy] == current_color:
                            break
                        grid[gridx][gridy] = current_color
                        gridx -= 1
                        gridy -= 1
            if dir == 4:  # check left
                ret = self._continued_check(grid, action, dir, current_color)
                if ret == 1:
                    gridy = y - 1
                    while gridy > 0:
                        if (grid[x][gridy] == current_color):
                            break
                        grid[x][gridy] = current_color
                        gridy -= 1
            if dir == 5:  # check bottom left
                ret = self._continued_check(grid, action, dir, current_color)
                if (ret == 1):
                    gridx, gridy = x + 1, y - 1
                    while gridx < self.size and gridy > 0:
                        if grid[gridx][gridy] == current_color:
                            break
                        grid[gridx][gridy] = current_color
                        gridx += 1
                        gridy -= 1
            if dir == 6:  # check downwards
                ret = self._continued_check(grid, action, dir, current_color)
                if (ret == 1):
                    gridx = x + 1
                    while gridx < self.size:
                        if grid[gridx][y] == current_color:
                            break
                        grid[gridx][y] = current_color
                        gridx += 1
            if dir == 7:  # check bottom right
                ret = self._continued_check(grid, action, dir, current_color)
                if (ret == 1):
                    gridx = x + 1
                    gridy = y + 1
                    while gridx < self.size and gridy < self.size:
                        if grid[gridx][gridy] == current_color:
                            break
                        grid[gridx][gridy] = current_color
                        gridx += 1
                        gridy += 1
        return grid

    # Helper method for update_grid(). Continue checking in each specified direction.
    # Return 0 if no conversions can be made
    # Return 1 if conversions can be made
    # Return 2 if it ends on a blank space
    def _continued_check(self, grid, action, dir, current_color):
        x, y = action
        if dir == 0 and y != self.size - 1:  # Check right
            if grid[x][y + 1] == 0:
                return 2
            elif grid[x][y + 1] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x, y + 1), dir, current_color)
                return ret
        elif dir == 1 and y != self.size - 1 and x != 0:  # Check top right
            if grid[x - 1][y + 1] == 0:
                return 2
            elif grid[x - 1][y + 1] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x - 1, y + 1), dir, current_color)
                return ret
        elif dir == 2 and x != 0:  # Check upwards
            if grid[x - 1][y] == 0:
                return 2
            elif grid[x - 1][y] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x - 1, y), dir, current_color)
                return ret
        elif dir == 3 and x != 0 and y != 0:  # Check top left
            if grid[x - 1][y - 1] == 0:
                return 2
            elif grid[x - 1][y - 1] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x - 1, y - 1), dir, current_color)
                return ret
        elif dir == 4 and y != 0:  # Check left
            if grid[x][y - 1] == 0:
                return 2
            elif grid[x][y - 1] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x, y - 1), dir, current_color)
                return ret
        elif dir == 5 and x != self.size - 1 and y != 0:  # Check bottom left
            if grid[x + 1][y - 1] == 0:
                return 2
            elif grid[x + 1][y - 1] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x + 1, y - 1), dir, current_color)
                return ret
        elif dir == 6 and x != self.size - 1:  # Check downwards
            if grid[x + 1][y] == 0:
                return 2
            elif grid[x + 1][y] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x + 1, y), dir, current_color)
                return ret
        elif dir == 7 and x != self.size - 1 and y != self.size - 1:  # Check bottom right
            if grid[x + 1][y + 1] == 0:
                return 2
            elif grid[x + 1][y + 1] == current_color:
                return 1
            else:
                ret = self._continued_check(grid, (x + 1, y + 1), dir, current_color)
                return ret
        return 0  # return 0 if none of the if statements were checked

    def update_action_space(self, grid):
        action_space = []
        if self.white_move:
            for x in range(self.size):
                for y in range(self.size):
                    if grid[x][y] == Reversi.WHITE:
                        for dir in range(8):
                            ret = self._continued_check(grid, (x, y), dir, Reversi.WHITE)
                            if ret == 2:
                                action_space = self._check_direction(grid, (x, y), action_space, dir)
        else:
            for x in range(self.size):
                for y in range(self.size):
                    if grid[x][y] == Reversi.BLACK:
                        for dir in range(8):
                            ret = self._continued_check(grid, (x, y), dir, Reversi.BLACK)
                            if ret == 2:
                                action_space = self._check_direction(grid, (x, y), action_space, dir)
        return action_space

    # Helper method to check the direction when updating action_space
    def _check_direction(self, grid, action, action_space, dir):
        x, y = action
        if dir == 0:  # Check right
            gridy = y + 1
            while gridy < self.size:
                if grid[x][gridy] == Reversi.EMPTY and gridy != y + 1:
                    action_space.append((x, gridy))
                    break
                elif grid[x][gridy] == Reversi.EMPTY and gridy == y + 1:
                    break
                gridy += 1
        if dir == 1:  # Check top right
            gridx, gridy = x - 1, y + 1
            while gridx >= 0 and gridy < self.size:
                if grid[gridx][gridy] == Reversi.EMPTY and gridy != y + 1 and gridx != x - 1:
                    action_space.append((gridx, gridy))
                    break
                elif grid[gridx][gridy] == Reversi.EMPTY and gridy == y + 1 and gridx == x - 1:
                    break
                gridy += 1
                gridx -= 1
        if dir == 2:  # Check upward
            gridx = x - 1
            while gridx >= 0:
                if grid[gridx][y] == Reversi.EMPTY and gridx != x - 1:
                    action_space.append((gridx, y))
                    break
                elif grid[gridx][y] == Reversi.EMPTY and gridx == x - 1:
                    break
                gridx -= 1
        if dir == 3:  # Check top left
            gridx, gridy = x - 1, y - 1
            while gridx >= 0 and gridy > 0:
                if grid[gridx][gridy] == Reversi.EMPTY and gridx != x - 1 and gridy != y - 1:
                    action_space.append((gridx, gridy))
                    break
                elif grid[gridx][gridy] == Reversi.EMPTY and gridx == x - 1 and gridy == y - 1:
                    break
                gridx -= 1
                gridy -= 1
        if dir == 4:  # Check left
            gridy = y - 1
            while gridy >= 0:
                if grid[x][gridy] == Reversi.EMPTY and gridy != y - 1:
                    action_space.append((x, gridy))
                    break
                elif grid[x][gridy] == Reversi.EMPTY and gridy == y - 1:
                    break
                gridy -= 1
        if dir == 5:  # Check bottom left
            gridx, gridy = x + 1, y - 1
            while gridx < self.size and gridy >= 0:
                if grid[gridx][gridy] == Reversi.EMPTY and gridx != x + 1 and gridy != y - 1:
                    action_space.append((gridx, gridy))
                    break
                elif grid[gridx][gridy] == Reversi.EMPTY and gridx == x + 1 and gridy == y - 1:
                    break
                gridx += 1
                gridy -= 1
        if dir == 6:  # Check downward
            gridx = x + 1
            while gridx < self.size:
                if grid[gridx][y] == Reversi.EMPTY and gridx != x + 1:
                    action_space.append((gridx, y))
                    break
                elif grid[gridx][y] == Reversi.EMPTY and gridx == x + 1:
                    break
                gridx += 1
        if dir == 7:  # Check bottom right
            gridx, gridy = x + 1, y + 1
            while gridx < self.size and gridy < self.size:
                if grid[gridx][gridy] == Reversi.EMPTY and gridx != x + 1 and gridy != y + 1:
                    action_space.append((gridx, gridy))
                    break
                elif grid[gridx][gridy] == Reversi.EMPTY and gridx == x + 1 and gridy == y + 1:
                    break
                gridx += 1
                gridy += 1
        return action_space
    def reset(self):
        pass

    def rendor(self):
        for row in self.grid:
            print(row)
        print("1: White piece")
        print("2: Black piece")


if __name__ == "__main__":
    r = Reversi(8)
    r.rendor()
