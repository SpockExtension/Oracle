from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/nonce')
def get_nonces():
    with open('nonce.txt', 'r') as f:
        nonces = [line.strip() for line in f.readlines()]
    return jsonify(nonces)

if __name__ == '__main__':
    app.run(debug=True)
