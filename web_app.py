from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    streak = db.Column(db.Integer, default=0)
    last_check_in = db.Column(db.DateTime)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([{
        'id': habit.id,
        'name': habit.name,
        'streak': habit.streak,
        'last_check_in': habit.last_check_in.isoformat() if habit.last_check_in else None
    } for habit in habits])

@app.route('/api/habits', methods=['POST'])
def add_habit():
    data = request.json
    habit = Habit(name=data['name'])
    db.session.add(habit)
    db.session.commit()
    return jsonify({
        'id': habit.id,
        'name': habit.name,
        'streak': habit.streak,
        'last_check_in': None
    })

@app.route('/api/habits/<int:habit_id>/check-in', methods=['POST'])
def check_in(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    now = datetime.utcnow()
    
    if habit.last_check_in:
        days_diff = (now - habit.last_check_in).days
        if days_diff == 1:  # consecutive day
            habit.streak += 1
        elif days_diff > 1:  # streak broken
            habit.streak = 1
    else:
        habit.streak = 1
    
    habit.last_check_in = now
    db.session.commit()
    
    return jsonify({
        'id': habit.id,
        'name': habit.name,
        'streak': habit.streak,
        'last_check_in': habit.last_check_in.isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
