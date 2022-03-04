import math

from board import play_game
from board import (Board, BoardCache, X, O, X_WINS,
                   O_WINS, is_draw)

#initialiaze a cache for the boards
nodecache = BoardCache()


class Node:
    """Class that defines a node of the tree search"""
    def __init__(self):
        self.parents = BoardCache()
        self.visits = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def add_parent_node(self, node_cache, parent_board):
        """add parent to the node"""
        result, found = self.parents.get_for_position(parent_board)
        if found is False:
            parent_node = find_or_create_node(node_cache, parent_board)
            self.parents.set_for_position(parent_board, parent_node)

    def get_tot_visits_parent_nodes(self):
        """returns total visits of parent node"""
        return sum([parent_node.visits for parent_node
                    in self.parents.cache.values()])

    def value(self):
        if self.visits == 0:
            return 0

        success_percentage = (self.wins + self.draws) / self.visits
        return success_percentage


def play_game_and_reset_playouts(x_strategy, o_strategy, node_cache=nodecache):
    """play game and reset to original state of board"""
    node_cache.reset()
    board = play_game(x_strategy, o_strategy)
    node_cache.reset()
    return board



def play_mcts_move(board, node_cache=nodecache):
    """play move dictated by mcts"""
    move_index_node_pairs = get_move_index_node_pairs(board, node_cache)
    move_index_to_play = max(move_index_node_pairs,
                             key=lambda pair: pair[1].value())[0]
    return board.move(move_index_to_play)


def get_move_index_node_pairs(board, node_cache):
    """get move index and corresponding node"""
    boards = [board.move(mi) for mi in board.get_valid_moves_indexes()]
    nodes = [find_or_create_node(node_cache, b) for b in boards]

    return zip(board.get_valid_moves_indexes(), nodes)


def training_playouts(node_cache=nodecache, board=Board(), num_playouts=5000, display_progress=True):
    """performs training of mcts"""
    for game in range(num_playouts):
        game_playout(node_cache, board)
        if display_progress is True and (game+1) % (num_playouts / 10) == 0:
            print(f"{game+1}/{num_playouts} playouts...")


def game_playout(node_cache, board):
    """performs an unfolding of the game"""
    game_history = [board]

    while not board.is_gameover():
        move_index = choose_move(node_cache, board)
        board = board.move(move_index)
        game_history.append(board)

    backpropagate(node_cache, board, game_history)


def choose_move(node_cache, parent_board):
    """chooses move with highest value"""
    move_value_pairs = calculate_values(node_cache, parent_board)
    return max(move_value_pairs, key=lambda pair: pair[1])[0]


def calculate_values(node_cache, parent_board):
    """calculates the values of the legal moves"""
    child_boards = [parent_board.move(mi) for mi
                    in parent_board.get_valid_moves_indexes()]
    values = [calculate_value(node_cache, parent_board, cb) for cb
              in child_boards]
    return zip(parent_board.get_valid_moves_indexes(), values)


def calculate_value(node_cache, parent_board, board):
    """calculate the value of a node"""
    node = find_or_create_node(node_cache, board)
    node.add_parent_node(node_cache, parent_board)
    if node.visits == 0:
        return math.inf

    parent_node_visits = node.get_tot_visits_parent_nodes()

    assert node.visits <= parent_node_visits, \
        "child node visits should be a subset of visits to the parent node "

    exploration_term = (math.sqrt(2.0)
                        * math.sqrt(math.log(parent_node_visits) / node.visits))

    value = node.value() + exploration_term

    return value


def backpropagate(node_cache, final_board_position, game_history):
    """sends the value of a node to the root node"""
    for board in game_history:
        node = find_node(node_cache, board)
        node.visits += 1
        if is_win(board.get_turn(), final_board_position):
            node.wins += 1
        elif is_loss(board.get_turn(), final_board_position):
            node.losses += 1
        elif is_draw(final_board_position):
            node.draws += 1
        else:
            raise ValueError("Illegal game state")


def find_node(node_cache, board):
    """finds a node in the tree"""
    result, found = node_cache.get_for_position(board)
    assert found is True, "node must exist"
    node, _ = result
    return node


def find_or_create_node(node_cache, board):
    """finds a node or if it doesn't exists it creates one"""
    result, found = node_cache.get_for_position(board)
    if found is False:
        node = Node()
        node_cache.set_for_position(board, node)
        return node

    node, _ = result
    return node


def is_win(player, board):
    """returns True if 'player' has won the game"""
    result = board.get_result()
    return ((player == X and result == O_WINS)
            or (player == O and result == X_WINS))


def is_loss(player, board):
    """returns True if 'player' has lost the game"""
    result = board.get_result()
    return ((player == X and result == X_WINS)
            or (player == O and result == O_WINS))