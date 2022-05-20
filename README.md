# 3-Level-Smart-TicTacToe
Basically, the goal of the tic-tac-toe agent is to try to achieve a winning condition before
the player, as well as prevent the player from winning. For the agent to be able to win, it
needs to place 3 consecutive symbols X in a diagonal or vertical or horizontal manner.
The agent also needs to be smart ranging in different levels (Level 0, 1, 2). In order to do
this, the agent should have different algorithms in order to detect the player's moves.


From the initial empty 4x4 tic-tac-toe table, the player(O) and the agent(X) take turns in
placing their symbol on the map 3 consecutive times in diagonal, horizontal, or vertical
manner.


LEVEL 0:
For level 0, the agent can only make random moves in its turn, it cannot detect if it
is one tile away from winning as well as if the player is about to win. From the first
move to its succeeding move every time it places X on the board it is a randomly
generated move. However even if it makes random moves, it can still win if the
agent achieves a winning condition in the game board.

LEVEL 1:
For level 1, a hard-coded set of movements is implemented for the agent's
rationality. These movements depend on the human player’s moves each turn. Each
move of the player has a corresponding hard-coded move for the agent. The result
for this is that if the human player is one tile away from achieving a winning
condition, the agent’s next move is to block the last tile needed by the human
player from winning. In this level the agent can not only try to prevent the player
from winning, but it can also win if it achieves one of the winning conditions.

LEVEL 2:
For level 2, the agent is implemented with the MiniMax algorithm. This algorithm is
chosen for the agents because of its rationality in finding the best possible move
that the agent can make. It’s the best search algorithm in coming up with a strategy
to win a Tic-Tac-Toe game. The algorithm uses heuristics in finding the best strategy
and move to make, which also is dependent from the human payer move. This level
differs from the previous two levels since not only does it prevent the player from
winning, but the agent in this level also comes up with a strategy to achieve a
winning condition
