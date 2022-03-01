from tictactoe import TicTacToeGame

import numpy as np
from collections import defaultdict
import random

class MonteCarloTreeSearchNode(object):
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = self.state.get_action_space()
        self._possible_actions = self.state.get_action_space()

    def get_untried_actions(self):
        self._untried_actions = self.state.get_action_space()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def _expand(self):
        # print('DEBUG. Expanding')
        action = self._untried_actions.pop()
        while not self.state.is_action_legal(action):
            action = self._untried_actions.pop()
        self.state.step(action)
        next_state = self.state.copy()
        child_node = MonteCarloTreeSearchNode(next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def _is_terminal_node(self):
        victory_reached, _ = self.state._check_victory()
        return victory_reached

    def _rollout(self):
        # print('DEBUG. Roll-out')
        current_rollout_state = self.state
        reward = 0
        done = False
        while not done:
            possible_moves = current_rollout_state.get_action_space()
            if possible_moves != []:
                action = random.choice(possible_moves)
                _, reward, done, _ = current_rollout_state.step(action)
                current_rollout_state.get_action_space()
        return reward

    def _backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent._backpropagate(result)

    def _is_fully_expanded(self):
        full_board = len(self.state.get_action_space()) == 0
        victory_reached, _ = self.state._check_victory()
        return full_board or victory_reached

    def _get_best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node._is_terminal_node():
            if not current_node._is_fully_expanded():
                return current_node._expand()
            else:
                current_node = current_node._get_best_child()
        return current_node

    def get_best_action(self, simulation_steps=100):
        for _ in range(simulation_steps):
            v = self._tree_policy()
            reward = v._rollout()
            v._backpropagate(reward)
        return self._get_best_child(c_param=0.).parent_action


def main():
    game = TicTacToeGame(3)
    game.reset()
    initial_state = game
    root = MonteCarloTreeSearchNode(state=initial_state)
    # TODD: Why the get_best_action() get stuck when simulation_steps is higher
    # than the board size (i.e. 9)?
    # TODD: Better understand the role of reward. As it is right now, it might
    # just make the entire algorithm fail.
    selected_node = root.get_best_action(10)
    print(selected_node)

if __name__ == '__main__':
    main()
