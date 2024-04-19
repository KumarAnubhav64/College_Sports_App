from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_login import UserMixin




db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10),nullable = True)
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        print( bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8')))
        print(password)
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum('game', 'practice', 'event'), nullable=False)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    given_by = db.Column(db.Integer, nullable=False)
    given_to = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

# Add models for other features (announcements, grievance, auction, players, games)