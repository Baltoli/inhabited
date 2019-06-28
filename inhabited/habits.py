from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from datetime import datetime

from inhabited.auth import login_required
from inhabited.db import get_db
from inhabited.completions import completed_periods, is_today, to_timestamp

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

    completions = [db.execute(
        'SELECT * FROM completion WHERE '
        ' habit_id = ?'
        ' ORDER BY timestamp DESC',
        (h['id'],)
    ).fetchall() for h in habits]

    periods = [
        completed_periods(10, c)
        for c in completions
    ]

    to_complete = [
        not p[0] for p in periods
    ]

    # Do the conversion logic here to turn timestamps into completion data -
    # probably will need a separate module in which I do these conversions based
    # on the current date, then pass to the templating engine etc

    return render_template('habits/index.html', data=zip(habits, periods, to_complete))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO habit (name, user_id) '
                'VALUES (?, ?)',
                (name, g.user['id'])
            )
            db.commit()
            return redirect(url_for('habits.index'))

    return render_template('habits/create.html')

def get_habit(id):
    habit = get_db().execute(
        'SELECT h.id, name, user_id, u.username '
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
        error = None

        if not name:
            error = 'Name is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE habit SET name = ?'
                ' WHERE id = ?',
                (name, id)
            )
            db.commit()
            return redirect(url_for('habits.index'))

    return render_template('habits/update.html', habit=habit)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_habit(id)
    db = get_db()
    db.execute('DELETE FROM habit WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('habits.index'))

def completed_today(habit_id):
    h = get_habit(id)
    db = get_db()
    ts = db.execute(
        'SELECT timestamp FROM completions '
        ' WHERE habit_id = ?'
        ' ORDER BY timestamp DESC'
    ).fetchone()['timestamp']
    return is_today(ts)

@bp.route('/<int:id>/complete', methods=('POST',))
@login_required
def complete(id):
    get_habit(id)
    db = get_db()
    db.execute(
        'INSERT INTO completion (habit_id, timestamp)'
        ' VALUES (?, ?)',
        (id, to_timestamp(datetime.now()))
    )
    db.commit()
    return redirect(url_for('habits.index'))
