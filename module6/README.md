# Game playing systems

## Implementation [Group]

* Implement tree search (Monte-Carlo or otherwise) in order to learn to win (or at least not lose) at the game Tic-tac-toe on the classic 3x3 grid. 
* You will have to make choices about
  * the roll-out policy of your player
  * the policy of your opponent
  * the selection policy in your search tree
  * the updates to your search tree ("back-up")
* Describe and motivate these choices briefly. For example, if you use a non-Monte-Carlo search, what did you use? If you use MC, how did you implement sampling?
* Evaluate your algorithm and comment on its pros and cons. For example, is it fast? Is it sample efficient? Is the learned policy competitive? Does it lose? Would you, as a human, beat it? Would it scale well to larger grids such as 4x4 or 5x5?

## TODOs

* How are the evaluation results collected?? 200 games?
* Is it sample efficient?
* Would you, as a human, beat it?
* Roll-out policy: our description is not sufficient.
* what does this sentence mean? Moreover, the more rounds the MCTS plays, the less chances there are to discard a win.