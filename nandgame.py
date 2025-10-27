from flask import Flask, request, render_template_string

app = Flask(__name__)

def nand(a, b):
    try:
        a = int(a)
        b = int(b)
        results = {
            "AND": str(a * b),
            "OR": str(a + b - a * b),
            "XOR": str(a + b - 2 * a * b),
            "NAND": str(1 - a * b),
            "NOR": str(1 - a - b + a * b),
            "XNOR": str(1 - a - b + 2 * a * b)
        }
        return results
    except ValueError:
        return {'Error': '整数を入力してください'}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        v1 = request.form.get('value1')
        v2 = request.form.get('value2')
        results = nand(v1, v2)
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
                box-sizing: border-box;
            }
            h1 {
                color: #3498db;
            }
            .container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 400px;
                box-sizing: border-box;
                margin-bottom: 20px;
            }
            p {
                margin: 10px 0;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .ad-container {
                width: 100%;
                text-align: center;
            }
            .form-group {
                margin-bottom: 15px;
                text-align: left;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input[type="text"] {
                width: calc(100% - 12px);
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                box-sizing: border-box;
            }
            button[type="submit"] {
                background-color: #3498db;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button[type="submit"]:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>論理演算</h1>
            <form method="POST">
                <div class="form-group">
                    <label for="value1">値1:</label>
                    <input type="text" id="value1" name="value1" required>
                </div>
                <div class="form-group">
                    <label for="value2">値2:</label>
                    <input type="text" id="value2" name="value2" required>
                </div>
                <button type="submit">計算</button>
            </form>
            {% if results %}
            <h2>計算結果</h2>
            {% for key, value in results.items() %}
                {% if key != 'Error' %}
                    <p>{{ key }}: {{ value }}</p>
                {% endif %}
            {% endfor %}
            {% if 'Error' in results %}
                <p style="color:red;">{{ results['Error'] }}</p>
            {% endif %}
            {% endif %}
        </div>
        <div class="ad-container">
            </div>
    </body>
    </html>
    """, results=results)

if __name__ == '__main__':
    app.run(debug=True)
