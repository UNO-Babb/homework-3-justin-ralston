from flask import Flask, render_template, session, redirect, url_for, request
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something random

# Game logic
SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

def init_game():
    session['player1'] = 1
    session['player2'] = 1
    session['turn'] = 1  # 1 for player1, 2 for player2
    session['message'] = ''

@app.route('/')
def index():
    if 'player1' not in session:
        init_game()

    return render_template(
        'index.html',
        player1=session['player1'],
        player2=session['player2'],
        turn=session['turn'],
        message=session.get('message', '')
    )

@app.route('/roll', methods=['POST'])
def roll():
    if 'player1' not in session:
        init_game()

    turn = session['turn']
    roll = random.randint(1, 6)
    message = f"Player {turn} rolled a {roll}."

    # Move player
    if turn == 1:
        session['player1'] += roll
        if session['player1'] in SNAKES:
            session['player1'] = SNAKES[session['player1']]
            message += f" Oh no! Player 1 hit a snake!"
        elif session['player1'] in LADDERS:
            session['player1'] = LADDERS[session['player1']]
            message += f" Yay! Player 1 climbed a ladder!"
        if session['player1'] >= 100:
            message = "🎉 Player 1 wins! Game over."
            init_game()
            session['message'] = message
            return redirect(url_for('index'))
        session['turn'] = 2
    else:
        session['player2'] += roll
        if session['player2'] in SNAKES:
            session['player2'] = SNAKES[session['player2']]
            message += f" Oh no! Player 2 hit a snake!"
        elif session['player2'] in LADDERS:
            session['player2'] = LADDERS[session['player2']]
            message += f" Yay! Player 2 climbed a ladder!"
        if session['player2'] >= 100:
            message = "🎉 Player 2 wins! Game over."
            init_game()
            session['message'] = message
            return redirect(url_for('index'))
        session['turn'] = 1

    session['message'] = message
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    init_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
