from board import Board, X, O, X_WINS, O_WINS, DRAW
from mcts import MCTS

import itertools
import matplotlib.pyplot as plt

def calc_percentage(array, element):
    return array.count(element) / len(array)

def play_random_move(board):
    """Strategy to play random moves"""
    move = board.get_random_legal_move_index()
    return board.move(move)

def play_human_move(board):
    """Strategy that requires human input"""
    print('Type move coordinates as (n, m): ')
    line = input()
    print(type(line))
    line = re.sub("[()]", "", line)
    bits = line.split(',')  # split
    bits = [int(bit) for bit in bits]
    move = np.ravel_multi_index(bits, board.get_board_dimensions())
    return board.move(move)

def play_single_game(x_strategy, o_strategy, board_size=3, verbose=0):
    """given the two players strategies it plays a game of tic-tac-toe"""
    board = Board(board_size=board_size)
    player_strategies = itertools.cycle([x_strategy, o_strategy])
    while not board.is_gameover():
        board = next(player_strategies)(board)
        if verbose:
            board.print_board()
    if verbose:
        board.print_board()
        print(result_dict.get(board.get_result()))
    return board

def play_games(total_games, x_strategy, o_strategy):
    """Plays a given number of games"""
    results = {
        X_WINS: 0,
        O_WINS: 0,
        DRAW: 0
    }
    results_array = []
    for g in range(total_games):
        end_of_game = play_single_game(x_strategy, o_strategy)
        result = end_of_game.get_result()
        results[result] += 1
        results_array.append(result)
    x_wins_percent = results[X_WINS] / total_games * 100
    o_wins_percent = results[O_WINS] / total_games * 100
    draw_percent = results[DRAW] / total_games * 100
    print(f"X wins: {x_wins_percent:.2f}%")
    print(f"O wins: {o_wins_percent:.2f}%")
    print(f"draw  : {draw_percent:.2f}%")
    return results_array

def main():
        board_size = 3
        n_games = 200
        num_playouts = 1000

        mcts = MCTS(board_size)
        print(f'Training MCTS with board size of {board_size}x{board_size}...')
        mcts.train(num_playouts=num_playouts)
        print('Training done. Starting evaluation. Playing {n_games}')
        results = play_games(n_games, play_random_move, mcts.play)

        lost_percentages = []
        win_percentages = []
        draw_percentages = []

        for i in range(len(results)):
            draw_percentages.append(calc_percentage(results[0:i + 1], 0))
            win_percentages.append(calc_percentage(results[0:i + 1], -1))
            lost_percentages.append(calc_percentage(results[0:i + 1], 1))

        plt.subplot()
        plt.plot(range(n_games), draw_percentages, color='orange', label='Draws')
        plt.plot(range(n_games), win_percentages, color='green', label='Wins')
        plt.plot(range(n_games), lost_percentages, color='red', label='Losses')
        plt.title(f'Draws/Wins/Losses Ratios for MCTS vs. Random Player')
        plt.xlabel(f'Number of games ({num_playouts} playouts per game)')
        plt.ylabel('Percentage Ratio')
        plt.legend()
        plt.grid(axis='y')
        plt.savefig(f'percentages_{board_size}x{board_size}.pdf')
        # plt.show()

        print('GAME OVER')


if __name__ == '__main__':
    main()


