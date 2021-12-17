from game import Board, Game
from policy_value_net_numpy import PolicyValueNetNumpy
from human_play import Human
from mcts_alphaZero import MCTSPlayer
import pickle
from flask import Flask, render_template, jsonify, request, current_app

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def func(data, board):
    location = "{}, {}".format(7 - data["stone"][0], data["stone"][1])
    if isinstance(location, str):  # for python3
        location = [int(n, 10) for n in location.split(",")]
    move = board.location_to_move(location)
    return move


@app.route("/ajax", methods=["POST"])
def ajax(board):
    data = request.get_json()  # spot data from index.html
    print(data)
    print(data)
    print(data)
    print(data)
    answer = func(data, board)
    return jsonify(result="success", result2=answer)


def run():
    board = Board(width=8, height=8, n_in_row=5)
    game = Game(board)

    try:
        policy_param = pickle.load(open("best_policy_8_8_5.model", "rb"))
    except:
        policy_param = pickle.load(
            open("best_policy_8_8_5.model", "rb"), encoding="bytes"
        )  # To support python3
    best_policy = PolicyValueNetNumpy(8, 8, policy_param)

    player1 = Human()
    player2 = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

    # keep available moves in a list
    availables = list(range(8 * 8))
    states = {}

    players = [1, 2]
    p1, p2 = players
    current_player = players[0]
    players = {p1: player1, p2: player2}
    player1.set_player_ind(p1)
    player2.set_player_ind(p2)
    count = 0
    while True:
        current_player = 1 if current_player != 1 else 0
        move = ajax(board)
        states[move] = current_player
        availables.remove(move)
        x = move // 8
        y = move % 8
        x = 7 - x
        post_data = (x, y)
        if count % 2 == 0:
            print(post_data)
        current_player = players[0] if current_player == players[1] else players[1]
        count += 1
        # end, winner = Game.board.game_end()
        # if end:
        #     if is_shown:
        #         if winner != -1:
        #             print("Game end. Winner is", players[winner])
        #         else:
        #             print("Game end. Tie")
        #     print(winner)


if __name__ == "__main__":
    app.run(debug=True)
    run()
