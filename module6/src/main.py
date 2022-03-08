from board import play_game, play_random_move, play_games, play_human_move
from mcts import play_mcts_move, training_playouts
import matplotlib.pyplot as plt


def calc_percentage(array, element):
    return array.count(element) / len(array)

def main():
        n_games = 200

        print('Training MCTS\n')
        training_playouts(num_playouts=1000)
        print('Random vs MCTS:\n')
        results = play_games(n_games,play_random_move, play_mcts_move)

        lost_percentages = []
        win_percentages = []
        draw_percentages = []

        for i in range(len(results)):
            draw_percentages.append(calc_percentage(results[0:i + 1], 0))
            win_percentages.append(calc_percentage(results[0:i + 1], -1))
            lost_percentages.append(calc_percentage(results[0:i + 1], 1))

        plt.subplot()
        plt.plot(range(n_games), draw_percentages, color='orange')
        plt.plot(range(n_games), win_percentages, color='green')
        plt.plot(range(n_games), lost_percentages, color='red')
        plt.savefig('percentages.png')
        plt.show()

        print('GAME OVER')


if __name__ == '__main__':
    main()


