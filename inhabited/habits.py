from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from inhabited.auth import login_required
from inhabited.db import get_db

bp = Blueprint('habits', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()

    habits = db.execute(
        'SELECT id, name '
        'FROM habit WHERE user_id = ?',
        (g.user['id'],)
    ).fetchall()

    return render_template('habits/index.html', habits=habits)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        period = request.form['period']
        error = None

        if not name:
            error = 'Name is required'

        if not period:
            error = 'Period is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO habit (name, period, user_id) '
                'VALUES (?, ?, ?)',
                (name, period, g.user['id'])
            )
            db.commit()
            return redirect(url_for('habits.index'))

    return render_template('habits/create.html')
