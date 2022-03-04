from board import play_game, play_random_move, play_games, play_human_move
from mcts import play_mcts_move, training_playouts


print('Training MCTS\n')
training_playouts()
print('Random vs MCTS:\n')
play_games(20000,play_random_move,play_mcts_move)
print('GAME OVER')