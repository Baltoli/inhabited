from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from inhabited.auth import login_required
from inhabited.db import get_db

bp = Blueprint('habits', __name__)

@bp.route('/')
def index():
    db = get_db()
    habits = db.execute(
        # query here
    ).fetchall()
    return render_template('habits/index.html', habits=habits)
