import random
import numpy as np

class RuleBasedPlayer(object):
    """docstring for RuleBasedPlayer"""
    def __init__(self, grid_size=3, player_id=2):
        super(RuleBasedPlayer, self).__init__()
        self.grid_size = grid_size
        self.player_id = player_id

    def get_action(self, observation, playstyle='random'):
        def get_random_move():
            possible_actions = []
            for i, row in enumerate(observation):
                for j, cell in enumerate(row):
                    if cell == 0:
                        possible_actions.append((i, j))
            return random.choice(possible_actions)

        if playstyle == 'first_available':
            for i, row in enumerate(observation):
                for j, cell in enumerate(row):
                    if cell == 0:
                        return i, j
        elif playstyle == 'optimum':
            if not np.any(observation):
                # First turn, the board is still clear, place it in a corner
                return (0, 0)
            else:
                center = (self.grid_size // 2, self.grid_size // 2)
                if observation[center] == 0:
                    return center
                return get_random_move()
        else: # Random
            possible_actions = []
            for i, row in enumerate(observation):
                for j, cell in enumerate(row):
                    if cell == 0:
                        possible_actions.append((i, j))
            return random.choice(possible_actions)