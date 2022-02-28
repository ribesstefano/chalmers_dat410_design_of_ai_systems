import numpy as np
from collections import defaultdict
from tictactoe import TicTacToeGame


class MonteCarloTreeSearch(object):
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[2] = 0
        self.untried_actions = None
        self.untried_actions = self.remaining_actions()
        return

    def remaining_actions(self):
        return self.get_legal_actions()

    def q(self):
        #difference in number of win and losses
        wins = self.results[1]
        losses = self.results[2]
        return wins - losses

    def n(self):
        return self.number_of_visits

    def expand(self):
        action = self.untried_actions
        next_state = self.state.step(action)
        child_node = MonteCarloTreeSearch(next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.is_game_over()

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=0.1):

        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    def get_legal_actions(self):
        return self.state.board[self.state.board == 0]

    def is_game_over(self):
        legal_actions =  self.get_legal_actions()
        legal_actions = list(legal_actions)
        if bool(legal_actions):
            return False
        else:
            return True

    def game_result(self):
        _, result = tictactoe._check_victory(self.state)
        return result

    def move(self, action):
        self.state = tictactoe.step(action)
        return self.state


def main():
    grid_size = 3
    initial_state = TicTacToeGame(grid_size)
    root = MonteCarloTreeSearch(initial_state)
    best_move = root.best_action()


if __name__ == '__main__':
    main()
