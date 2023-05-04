from flask import Flask, request
import csv

app = Flask(__name__)

users = {}

@app.route('/add_user/<username>/<public_key>', methods=['POST'])
def add_user(username, public_key):
    if username is not None and public_key is not None:
        with open('keypairs.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username:
                    return "User already exists", 400

        users[username] = public_key

        # Write the new user to keypairs.csv
        with open('keypairs.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([username, public_key])

        return "User added successfully", 200
    else:
        return "Invalid request", 400


if __name__ == '__main__':
    app.run(port=9694)
