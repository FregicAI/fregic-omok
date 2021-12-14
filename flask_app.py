from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 유저가 클릭한 좌표 입력받아서 ai가 착수한 좌표 가져오는 함수
def plus_1(a, b):
    return [a + 1, b + 1]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax", methods=["POST"])
def ajax():
    data = request.get_json()
    print(data["stone"])
    answer = plus_1(data["stone"][0], data["stone"][1])
    return jsonify(result="success", result2=answer)


if __name__ == "__main__":
    app.run(debug=True)

