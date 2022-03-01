import itertools
import numpy as np
import copy

class TicTacToeGame(object):
    """
    docstring for TicTacToeGame
    """
    def __init__(self, grid_size=3, bot_player_id=1, num_players=2):
        super(TicTacToeGame, self).__init__()
        self.grid_size = grid_size
        self.num_players = num_players
        self.bot_player_id = bot_player_id
        self.board = [[0] * self.grid_size] * self.grid_size
        self.board = np.zeros((self.grid_size, self.grid_size))
        coords = [x for x in range(grid_size)]
        self.action_space = list(itertools.product(coords, coords))
        self.observation_space = [[0] * self.grid_size] * self.grid_size
        self.player_turn = 1
        self.num_turns_passed = 0
        self.max_num_turns = grid_size ** 2
        assert 0 < self.bot_player_id <= num_players, f'ERROR. Bot ID {self.bot_player_id} higher than number of players ({self.num_players}).'
    
    def reset(self):
        coords = [x for x in range(self.grid_size)]
        self.action_space = list(itertools.product(coords, coords))
        self.board = np.zeros((self.grid_size, self.grid_size))
        self.player_turn = 1
        self.num_turns_passed = 0

    def get_action_space(self):
        return self.action_space.copy()

    def _check_victory(self):
        # Get the two diagonals
        main_diag = np.diag(self.board)
        opposite_diag = np.diag(np.fliplr(self.board))
        # For each player, check all the possible winning conditions
        for player_id in range(1, self.num_players + 1):
            if np.all(main_diag == player_id):
                return True, player_id
            if np.all(opposite_diag == player_id):
                return True, player_id
            check_line = lambda x: np.all(x == player_id)
            # Check the columns
            if any(np.apply_along_axis(check_line, axis=0, arr=self.board)):
                return True, player_id
            # Check the rows
            if any(np.apply_along_axis(check_line, axis=1, arr=self.board)):
                return True, player_id
        # If the board is full, stop the game anyway
        if self.num_turns_passed == self.max_num_turns:
            return True, 0
        else:
            return False, 0

    def _get_reward(self, done, winning_player):
        # TODO: This function is bindly counting the number of cells belonging
        # to the bot player. However, it should also consider the taken action.
        # In fact, if the bot had the chance to win and instead placed the toe
        # in a non-winning cell, then the reward can still be high!!!
        reward = 0
        if done and self.bot_player_id == winning_player:
            return self.grid_size ** 3
        # For the bot player, count the number of winning conditions which are
        # close to achieve. E.g. If a row has 2 out 3 cells belonging to the bot
        # player, then the reward would be +2.
        # Check diagonals
        reward += (np.diag(self.board) == self.bot_player_id).sum()
        reward += (np.diag(np.fliplr(self.board)) == self.bot_player_id).sum()
        # Check rows and columns
        count_toes = lambda x: (x == self.bot_player_id).sum()
        reward += np.apply_along_axis(count_toes, axis=0, arr=self.board).sum()
        reward += np.apply_along_axis(count_toes, axis=1, arr=self.board).sum()
        return reward

    def is_action_legal(self, action):
        if action in self.action_space and self.board[action] == 0:
            return True
        else:
            return False

    def step(self, action, verbose=0):
        assert action in self.action_space, f'ERROR. Cell {action} outside of the board.'
        assert self.board[action] == 0, f'ERROR. Cell {action} already occupied.'
        self.action_space.remove(action)
        self.num_turns_passed += 1
        if verbose:
            print(f'DEBUG. Player {self.player_turn} selecting cell {action}')
        self.board[action] = self.player_turn
        if self.player_turn == self.num_players:
            self.player_turn = 1
        else:
            self.player_turn += 1
        observation = self.board
        done, winning_player = self._check_victory()
        reward = self._get_reward(done, winning_player)
        return observation, reward, done, {}

    def render(self):
        print('-' * 3 * self.grid_size)
        for row in self.board:
            for cell in row:
                if cell == 1:
                    toe = 'X'
                elif cell == 2:
                    toe = 'O'
                else:
                    toe = ' '
                print(f'[{toe}]', end='')
            print('')
        print('-' * 3 * self.grid_size)

    def __copy__(self):
        new_env = TicTacToeGame(self.grid_size, self.bot_player_id, self.num_players)
        new_env.board = self.board.copy()
        new_env.action_space = self.action_space.copy()
        new_env.observation_space = self.observation_space.copy()
        new_env.player_turn = self.player_turn
        new_env.num_turns_passed = self.num_turns_passed
        new_env.max_num_turns = self.max_num_turns
        return new_env

    def copy(self):
        return self.__copy__()

def main():
    grid_size = 3
    env = TicTacToeGame(grid_size)
    env.reset()
    coords = [x for x in range(grid_size)]
    # for a in [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]:
    for a in list(itertools.product(coords, coords)):
        observation, reward, done, _ = env.step(a)
        env.render()
        print(f'Reward: {reward}')
        if done:
            break

if __name__ == '__main__':
    main()
