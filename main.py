from flask import Flask, render_template, jsonify,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/calender'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/calender')
def calender():
    return render_template('calender.html')



@app.route('/events')
def get_events():
    events = Event.query.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
        })
    return jsonify(event_list)

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form.get('title')
    start = request.form.get('start')

    new_event = Event(title=title, start=start)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('calender'))

@app.route("/live")
def live():
    live = 'https://www.youtube.com/embed/HscrSwilshM?si=_ViLRqfKtaW3oiWd'
    return render_template("live.html",live = live)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port= 5001,debug=True)


