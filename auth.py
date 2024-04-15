from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/auth'
db = SQLAlchemy(app)

# Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    db.create_all()  # Create tables based on models
    app.run(debug=True)
