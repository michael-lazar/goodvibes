import os
import random
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, url_for
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

load_dotenv()

_DEFAULT_FLASH_DIR = Path(__file__).parent / "static" / "flash"
FLASH_DIR = Path(os.environ.get("GOODVIBES_FLASH_DIR", _DEFAULT_FLASH_DIR))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["BASIC_AUTH_USERNAME"] = os.environ["BASIC_AUTH_USERNAME"]
app.config["BASIC_AUTH_PASSWORD"] = os.environ["BASIC_AUTH_PASSWORD"]

basic_auth = BasicAuth(app)
admin = Admin(app)


class FileView(FileAdmin):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise HTTPException("", basic_auth.challenge())
        return True


# Enable uploading & deleting flash files using the /admin endpoint
admin.add_view(FileView(str(FLASH_DIR), "/static/flash/"))


def _get_flashes():
    # Refresh on every request to support adding files to the directory
    return sorted(p.stem for p in FLASH_DIR.iterdir() if p.suffix == ".swf")


@app.route("/")
def get_index():
    flashes = _get_flashes()
    if not flashes:
        return "Flash directory is empty, add files to the server!"

    flash = random.choice(flashes)
    return redirect(url_for("get_flash", flash=flash))


@app.route("/f/<flash>")
def get_flash(flash=None):
    flashes = _get_flashes()
    if flash not in flashes:
        abort(404)

    index = flashes.index(flash)
    next_flash = flashes[(index + 1) % len(flashes)]
    prev_flash = flashes[(index - 1) % len(flashes)]
    return render_template(
        "index.html",
        flashes=flashes,
        flash_source=url_for("static", filename=f"flash/{flash}.swf"),
        next_flash=url_for("get_flash", flash=next_flash),
        prev_flash=url_for("get_flash", flash=prev_flash),
    )
