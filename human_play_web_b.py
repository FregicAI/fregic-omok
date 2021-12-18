from game import Game, Board
from policy_value_net_numpy import PolicyValueNetNumpy
from mcts_alphaZero import MCTSPlayer

from flask import Flask, render_template, jsonify, request
import pickle

app = Flask(__name__)


board = Board(width=8, height=8, n_in_row=5)
game = Game(board)

board.init_board(start_player=0)
players = [1, 2]
player1 = 1
player2 = 2
current_player = 1

try:
    policy_param = pickle.load(open("best_policy_8_8_5.model", "rb"))
except:
    policy_param = pickle.load(
        open("best_policy_8_8_5.model", "rb"), encoding="bytes"
    )  # To support python3
best_policy = PolicyValueNetNumpy(8, 8, policy_param)
mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax", methods=["POST"])
def ajax():
    data = request.get_json()  # spot data from index.html
    move = data["stone"][0] * 8 + data["stone"][1]
    board.do_move(move)
    ai_answer = mcts_player.get_action(board)
    answer = [int(ai_answer // 8), int(ai_answer % 8)]

    return jsonify(result="success", result2=answer)


if __name__ == "__main__":
    app.run(debug=True)

while True:
    if current_player == 1:
        with app.test_request_context("/ajax"):
            ajax()
    else:
        move = mcts_player.get_action(board)
        Game.board.do_move(move)
    current_player = player1 if current_player != player1 else player2
    end, winner = Game.board.game_end()
    if end:
        if winner != -1:
            print("Game end. Winner is", players[winner])
        else:
            print("Game end. Tie")
    print("winner")
    break
