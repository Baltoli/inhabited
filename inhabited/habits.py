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

def get_habit(id):
    habit = get_db().execute(
        'SELECT h.id, name, period, user_id, u.username '
        ' FROM habit h JOIN user u ON h.user_id = u.id'
        ' WHERE h.id = ?',
        (id,)
    ).fetchone()

    if habit is None:
        abort(404, "Habit id {0} doesn't exist".format(id))

    if habit['user_id'] != g.user['id']:
        abort(403)

    return habit

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    habit = get_habit(id)

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
                'UPDATE habit SET name = ?, period = ?'
                ' WHERE id = ?',
                (name, period, id)
            )
            db.commit()
            return redirect(url_for('habits.index'))

    return render_template('habits/update.html', habit=habit)
