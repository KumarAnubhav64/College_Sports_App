from flask import Flask, render_template, jsonify,request,redirect,url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from auth import login_manager, login_required,auth
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, User, Event,Inventory
from config import Config
import os

secret_key = os.urandom(24)
app = Flask(__name__)
app.secret_key = secret_key
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
app.register_blueprint(auth)

@app.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('auth.login'))

@app.route('/calendar')

def calendar():
    if current_user.is_authenticated:
        username = current_user.username
        role = current_user.role
        return render_template('calendar.html',username=username,role = role)
    else:
        return redirect(url_for('auth.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        username = current_user.username

        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('auth.login'))

@app.route('/events')
def get_events():
    events = Event.query.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end' : event.end_date.isoformat(),
            
        })
    return jsonify(event_list)

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form.get('title')
    start = request.form.get('start')
    end = request.form.get('end')
    type = request.form.get('type')
    new_event = Event(title=title, start_date=start,end_date = end,type= type)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('calendar'))

@app.route('/inventory')
def inventory():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    data = Inventory.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('inventory.html', data=data)



@app.route('/add_row', methods=['POST'])
def add_row():
    item_name = request.form.get('item_name')
    quantity = request.form.get('quantity')
    given_by = request.form.get('given_by')
    given_to = request.form.get('given_to')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    new_row = Inventory(
        item_name=item_name,
        quantity=quantity,
        given_by=given_by,
        given_to=given_to,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(new_row)
    db.session.commit()
    return jsonify({'message': 'Row added successfully'})


@app.route('/delete_row/<int:row_id>', methods=['DELETE'])
def delete_row(row_id):
    row_to_delete = Inventory.query.get_or_404(row_id)
    db.session.delete(row_to_delete)
    db.session.commit()
    return jsonify({'message': 'Row deleted successfully'})


@app.route("/live")
def live():
    live = 'https://www.youtube.com/embed/HscrSwilshM?si=_ViLRqfKtaW3oiWd'
    return render_template("live.html",live = live)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port= 5001,debug=True)



