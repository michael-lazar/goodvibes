import os
import random

from flask import Flask, render_template, url_for, redirect, abort

FLASH_DIR = os.path.join(os.path.dirname(__file__), 'static', 'flash')

app = Flask(__name__)


@app.route("/")
def get_index():
    flashes = sorted(f for f in os.listdir(FLASH_DIR) if f.endswith('.swf'))
    flash = random.choice(flashes)
    return redirect(url_for('get_flash', flash=flash))

@app.route("/<flash>")
def get_flash(flash=None):
    flashes = sorted(f for f in os.listdir(FLASH_DIR) if f.endswith('.swf'))
    if flash not in flashes:
        abort(404)
    
    index = flashes.index(flash)
    next_flash = flashes[(index + 1) % len(flashes)]
    prev_flash = flashes[(index - 1) % len(flashes)]
    return render_template(
        'index.html',
        flashes=flashes,
        flash_source=url_for('static', filename=os.path.join('flash', flash)),
        next_flash=url_for('get_flash', flash=next_flash),
        prev_flash=url_for('get_flash', flash=prev_flash))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
