from flask import Flask, render_template, request, redirect, url_for, session
import random
import time
import threading
from pygame import mixer

app = Flask(__name__)
app.secret_key = 'super secret key'

horses = ["クラウドナイト", "ダンディオン", "ルシフェルウィング",
          "アレスフレア", "レオンハート", "ゼウスブレイド"]
horse_images = [f"static/images/{i}.png" for i in range(1, 7)]
girl_images = ["static/images/7.png"]
prize_distribution = [200000000, 100000000, 100000000, 0, 0, 0]
initial_contributions = {horse: 0 for horse in horses}
previous_results = []
race_in_progress = False
scroll_thread = None

def format_money(amount):
    if amount >= 100000000:
        oku = amount // 100000000
        man = (amount % 100000000) // 10000
        if man == 0:
            return f"{oku}億円"
        else:
            return f"{oku}億{man}万円"
    elif amount >= 10000:
        return f"{amount // 10000}万円"
    return f"{amount}円"

def calculate_prize(contributions):
    sorted_horses = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    total_money = sum(contribution for _, contribution in sorted_horses[:3])
    prize_money = min(total_money, 300000000)
    return prize_money

def simulate_users():
    global race_in_progress
    n = 10
    while race_in_progress:
        time.sleep(n)
        horse_name = random.choice(horses)
        session['contributions'][horse_name] += 10000000
        n = max(1, n - 1)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', horses=horses, horse_images=horse_images,
                           girl_images=girl_images,
                           contributions=session.get('contributions', initial_contributions),
                           previous_results=previous_results,
                           skip_confirmation=session.get('skip_confirmation', False),
                           race_in_progress=race_in_progress,
                           format_money=format_money)  # format_money 関数をテンプレートに渡す

@app.route('/start_race', methods=['POST'])
def start_race():
    global race_in_progress, scroll_thread
    if race_in_progress:
        return redirect(url_for('index'))

    session['race_started'] = True
    race_in_progress = True
    session['race_result'] = None
    session['total_contribution'] = None

    threading.Thread(target=simulate_users, daemon=True).start()
    threading.Timer(15, generate_race_result).start()

    return redirect(url_for('index'))

def generate_race_result():
    global race_in_progress, previous_results
    race_in_progress = False
    contributions = session.get('contributions', initial_contributions).copy()
    race_result = sorted(horses, key=lambda x: contributions[x], reverse=True)
    prize_money_list = {horse: 0 for horse in horses}
    for i in range(min(len(race_result), len(prize_distribution))):
        prize_money_list[race_result[i]] = prize_distribution[i]

    session['race_result'] = [(horse, format_money(contributions[horse])) for horse in race_result]
    session['total_contribution'] = format_money(calculate_prize(contributions))
    previous_results.append(session['race_result'])
    session['contributions'] = initial_contributions.copy()

@app.route('/contribute/<horse_name>', methods=['POST'])
def contribute(horse_name):
    if not race_in_progress:
        if 'contributions' not in session:
            session['contributions'] = initial_contributions.copy()
        session['contributions'][horse_name] += 10000000
    return redirect(url_for('index'))

@app.route('/toggle_skip_confirmation', methods=['POST'])
def toggle_skip_confirmation():
    session['skip_confirmation'] = not session.get('skip_confirmation', False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
