import functools
import sqlite3
import werkzeug.exceptions
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, flash, render_template, request, session, url_for, current_app, g, redirect
from src import db, auth

bp = Blueprint('cookbook', __name__, url_prefix='cookbook')

@bp.route('/new', methods=('GET', 'POST'))
@auth.authorize_login
def new_recipe():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['recipe']
        keywords = request.form['keywords'].split(',')
        keywords_string = json.dumps(keywords)
        user_id = session.get('user_id')
        print(title)
        print(body)
        print(type(keywords), type(keywords_string))
        print(keywords_string)
        print(user_id)
        error = None

        conn = db.lite_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO recipe (title, recipe, keywords) VALUES (?,?,?);",
                        (title, body, keywords_string))
        except sqlite3.IntegrityError:
            error = "Recipe already exists!"
        conn.commit()
        cur.execute("SELECT id FROM recipe WHERE title=?;",
                    (title,))
        recipe_id = cur.fetchone()
        print(recipe_id[0])
        print(session['user_id'])
        # cur.execute("INSERT INTO user_recipe (user_id, recipe_id) VALUES (?,?);",
        #             (int(session[user_id]), int(recipe_id)))
        # conn = db.lite_conn()
        # cur = conn.cursor()
        if error:
            flash(error)
        else:
            flash("New recipe logged!")

        return redirect(url_for('web.cookbook'))
    
    return render_template('cookbook/new.html')