import os
import random

from flask import Flask, jsonify, render_template

STATIC = os.path.join(os.path.dirname(__file__), 'static')
FLASH = os.path.join(STATIC, 'flash')

app = Flask(__name__)

@app.route("/")
def get_index():
    files = [f for f in os.listdir(FLASH) if f.endswith('.swf')]
    filename = os.path.join('flash', random.choice(files))
    return render_template('index.html', filename=filename)

@app.route("/files")
def get_files():
    files = os.listdir(FLASH)
    return jsonify({'items': files})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
