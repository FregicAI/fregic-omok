from game import Game, Board
from policy_value_net_numpy import PolicyValueNetNumpy
from mcts_alphaZero import MCTSPlayer

from flask import Flask, render_template, jsonify, request
import pickle

app = Flask(__name__)


board = Board(width=15, height=15, n_in_row=5)
game = Game(board)

board.init_board(start_player=0)
players = [1, 2]
player1 = 1
player2 = 2
current_player = 1

try:
    policy_param = pickle.load(open("models/best_policy.model", "rb"))
except:
    policy_param = pickle.load(
        open("models/best_policy_8_8_5.model", "rb"), encoding="bytes"
    )  # To support python3
best_policy = PolicyValueNetNumpy(15, 15, policy_param)
mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax", methods=["POST"])
def ajax():
    data = request.get_json()  # spot data from index.html
    print(data)
    if data["message"] == "restart":
        board.init_board()
        return jsonify(result="success")
    elif data["message"] == "timeout":
        board.init_board()
        return jsonify(result="success")
    else:
        move = data["stone"][0] * 15 + data["stone"][1]
        board.do_move(move)
        ai_answer = mcts_player.get_action(board)
        board.do_move(ai_answer)
        answer = [int(ai_answer // 15), int(ai_answer % 15)]
        print("ai : {}".format(answer))

        return jsonify(result="success", result2=answer)


if __name__ == "__main__":
    app.run(debug=True)
