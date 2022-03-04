from tictactoe import TicTacToeGame
from rule_based_player import RuleBasedPlayer
from mcts import MonteCarloTreeSearchNode

import itertools
import random
import numpy as np

class MCTS(object):
    """docstring for MCTS"""
    def __init__(self):
        super(MCTS, self).__init__()
    
    def fit(self, env):
        pass

    def get_action(self, observation):
        check_free = lambda x: (x == 0).argmax()
        x = np.apply_along_axis(check_free, axis=0, arr=observation).argmax()
        y = np.apply_along_axis(check_free, axis=1, arr=observation).argmax()
        for i, row in enumerate(observation):
            for j, cell in enumerate(row):
                if cell == 0:
                    return i, j

def main():
    num_players = 2
    grid_size = 3
    env = TicTacToeGame(grid_size)
    model = MCTS()
    opponent = RuleBasedPlayer()
    num_tests = 100
    winning_reward = grid_size ** 3
    render_board = False
    num_winning_games = [0] * 2
    player_stats = {
        'won games' : 0,
        'played turns' : [],
    }
    stats = [player_stats] * num_players

    print('INFO. Training Monte Carlo tree search model.')
    model.fit(env)
    print('INFO. Starting game tests.')
    for i in range(num_tests):
        if i % int(num_tests * 0.1) == 0:
            print(f'DEBUG. Running game n.{i}, {i / num_tests * 100:.1f}% done.')
        env.reset()
        observation = np.zeros((grid_size, grid_size))
        initial_player = random.choice([1, 2]) # Randomly determine who starts
        done = False
        turns = 0
        while not done:
            if (turns + initial_player) % 2 == 0:
                # Bot turn
                # a = model.get_action(observation)
                mcts = MonteCarloTreeSearchNode(env.copy())
                a = mcts.get_best_action(2)
            else:
                # Our player turn
                a = random.choice(env.get_action_space())
                a = opponent.get_action(observation, 'optimum')
            observation, reward, done, _ = env.step(a)
            if reward == winning_reward:
                num_winning_games[(turns + initial_player) % 2] += 1
                stats[(turns + initial_player) % 2]['won games'] += 1
            turns += 1
            for j in range(num_players):
                stats[j]['played turns'].append(turns)
            if render_board:
                env.render()
    # Print statistics
    num_ties = num_tests - sum(num_winning_games)
    print(f'INFO. Number of played games: {num_tests}')
    print(f'INFO. Tied games: {num_ties}, tie rate: {num_ties / num_tests * 100:.1f}%')
    for i, score in enumerate(num_winning_games):
        player_type = 'bot' if i == 0 else 'opponent'
        print(f'INFO. Player n.{i+1} ({player_type}) won {score} games, winning rate: {score / num_tests * 100:.1f}%')

if __name__ == '__main__':
    main()