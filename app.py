from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    target_days = db.Column(db.Integer, default=21)
    current_streak = db.Column(db.Integer, default=0)
    last_check_in = db.Column(db.DateTime)

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    check_in_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)

@app.route('/add_habit', methods=['POST'])
def add_habit():
    name = request.form.get('name')
    description = request.form.get('description')
    target_days = int(request.form.get('target_days', 21))
    
    new_habit = Habit(name=name, description=description, target_days=target_days)
    db.session.add(new_habit)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/check_in/<int:habit_id>', methods=['POST'])
def check_in(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    now = datetime.utcnow()
    
    # Create new habit log
    log = HabitLog(habit_id=habit_id, check_in_date=now)
    db.session.add(log)
    
    # Update streak
    if habit.last_check_in:
        time_diff = now - habit.last_check_in
        if time_diff.days <= 1:  # If checked in consecutive days
            habit.current_streak += 1
        else:
            habit.current_streak = 1
    else:
        habit.current_streak = 1
    
    habit.last_check_in = now
    db.session.commit()
    
    return jsonify({
        'success': True,
        'current_streak': habit.current_streak
    })

@app.route('/static/sw.js')
def sw():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/static/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
