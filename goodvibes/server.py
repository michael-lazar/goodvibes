import os
import random

from flask import Flask, render_template, url_for, redirect, abort
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException


FLASH_DIR = os.path.join(os.path.dirname(__file__), 'static', 'flash')

app = Flask(__name__)
application = app  # Alias for mod_wsgi compatibility
app.config.from_pyfile('server.cfg')
basic_auth = BasicAuth(app)
admin = Admin(app)


class FileView(FileAdmin):

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise HTTPException('', basic_auth.challenge())
        return True


# Enable uploading & deleting flash files using the /admin endpoint
admin.add_view(FileView(FLASH_DIR, '/static/flash/'))


def _get_flashes():
    # Refresh on every request to support adding files to the directory
    flashes = (f for f in os.listdir(FLASH_DIR) if f.endswith('.swf'))
    return sorted(f[:-4] for f in flashes)


@app.route("/")
def get_index():
    flashes = _get_flashes()
    if not flashes:
        return "Flash directory is empty, add files to the server!"

    flash = random.choice(flashes)
    return redirect(url_for('get_flash', flash=flash))


@app.route('/f/')
@app.route("/f/<flash>")
def get_flash(flash=None):
    flashes = _get_flashes()
    if not flashes:
        return "Flash directory is empty, add files to the server!"

    flash = flash or random.choice(flashes)
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
