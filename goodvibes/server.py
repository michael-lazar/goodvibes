import os
import random

from flask import Flask, render_template, url_for, redirect, abort

app = Flask(__name__)

# Compatibility for mod_wsgi
application = app

def _get_flashes():
    # Refresh on every request to support adding files to the directory
    flash_dir = os.path.join(os.path.dirname(__file__), 'static', 'flash')
    flashes = (f for f in os.listdir(flash_dir) if f.endswith('.swf'))
    return sorted(f[:-4] for f in flashes)

@app.route("/")
def get_index():
    flashes = _get_flashes()
    flash = random.choice(flashes)
    return redirect(url_for('get_flash', flash=flash))

@app.route("/<flash>")
def get_flash(flash=None):
    flashes = _get_flashes()
    if flash not in flashes:
        abort(404)

    index = flashes.index(flash)
    source = os.path.join('flash', flash + '.swf')
    next_flash = flashes[(index + 1) % len(flashes)]
    prev_flash = flashes[(index - 1) % len(flashes)]
    return render_template(
        'index.html',
        flashes=flashes,
        flash_source=url_for('static', filename=source),
        next_flash=url_for('get_flash', flash=next_flash),
        prev_flash=url_for('get_flash', flash=prev_flash))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
