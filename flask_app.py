from flask import Flask, render_template, request, jsonify
import csv
import random
import os

print("Current working directory:", os.getcwd())

app = Flask(__name__)

def load_games():
    games = []
    with open(os.path.join(app.root_path, 'games.csv'), 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games.append(row)
    return games


# Load games from CSV
def load_games():
    file_path = os.path.join(os.path.dirname(__file__), 'games.csv')
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    games = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            games.append(row)
    return games

@app.route('/', methods=['GET', 'POST'])
def index():
    games = load_games()
    filtered_games = games
    players = request.form.get('players', '')
    difficulty = request.form.get('difficulty', '')

    if request.method == 'POST':
        if players:
            players = int(players)
            filtered_games = [game for game in games 
                              if int(game['players_min']) <= players <= int(game['players_max'])]
        if difficulty:
            filtered_games = [game for game in filtered_games 
                              if game['difficulty'] == difficulty]

    return render_template('index.html', games=filtered_games, selected_players=players, selected_difficulty=difficulty)

@app.route('/random')
def random_game():
    games = load_games()
    players = request.args.get('players', '')
    difficulty = request.args.get('difficulty', '')

    if players:
        players = int(players)
        games = [game for game in games 
                 if int(game['players_min']) <= players <= int(game['players_max'])]
    if difficulty:
        games = [game for game in games 
                 if game['difficulty'] == difficulty]

    if not games:
        return jsonify({'error': 'No games match the criteria'})

    chosen_game = random.choice(games)
    return jsonify({
        'name': chosen_game['name'],
        'players': f"{chosen_game['players_min']}-{chosen_game['players_max']}",
        'difficulty': chosen_game['difficulty']
    })