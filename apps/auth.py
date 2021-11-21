from inspect import _empty
from flask import Blueprint, request, redirect, flash, url_for, session, g
from flask.templating import render_template
from werkzeug.security import check_password_hash, generate_password_hash
import functools

from apps.model import model
import datetime


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    print("login required session", session)
    if not session['login']:
      return redirect(url_for('auth.login'))
    return view(**kwargs)
  return wrapped_view


@bp.before_app_first_request
def load_logged_in_user():
  user_id = session.get('user_id')
  if user_id is None:
    session['user'] = None
  else:
    model.MyUser.query.filter_by(id=user_id).one()



@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    error = None

    if not email:
      error = '이메일을 입력해주세요'
    elif not password:
      error = '비밀번호를 입력해주세요'

    try:
      data = model.MyUser(
        email= email,
        password = generate_password_hash(password),
        created_at=datetime.datetime.now().replace(tzinfo=None),
        updated_at=datetime.datetime.now().replace(tzinfo=None),
      )
      select_user = model.MyUser.query.filter_by(email = request.form['email']).all()
      if len(select_user) > 0:
          error = "이미 사용 중인 이메일입니다."
      if error is None:
        model.db.session.add(data)
        model.db.session.commit()
        model.db.session.remove()
        return redirect(url_for('auth.login'))
    except Exception as e:
      return str(e)
    flash(error)
  return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
  if session['login']== True:
    return redirect(url_for('index'))

  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    error = None

    user = model.MyUser.query.filter_by(email=email).one()
    print("user", user.id)
    if user is None:
      error = "이메일을 다시 확인해주세요"
    elif not check_password_hash(user.password, password):
      error = "비밀번호를 다시 확인해주세요"

    if error is None:
      session.clear()
      session['user_id'] = user.id
      session['email'] = user.email
      session['login'] = True
      return redirect(url_for('index'))
    flash(error)
  return render_template('auth/login.html')


@bp.route('/logout')
def logout():
  session.clear()
  session['login'] = False
  print("session", session)
  return redirect(url_for('auth.login'))