import os

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def get_index():
    flash_dir = os.path.join(os.path.dirname(__file__), 'static', 'flash')
    videos = [f for f in os.listdir(flash_dir) if f.endswith('.swf')]
    return render_template('index.html', videos=videos)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
