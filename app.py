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

# 确保数据库存在
with app.app_context():
    if not os.path.exists('habits.db'):
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
    
    # 创建新的打卡记录
    log = HabitLog(habit_id=habit_id, check_in_date=now)
    db.session.add(log)
    
    # 更新连续天数
    if habit.last_check_in:
        days_diff = (now.date() - habit.last_check_in.date()).days
        if days_diff == 1:  # 连续打卡
            habit.current_streak += 1
        elif days_diff == 0:  # 今天已经打卡
            return jsonify({'error': '今天已经打卡了'}), 400
        else:  # 断签，重新开始计数
            habit.current_streak = 1
    else:
        habit.current_streak = 1
    
    habit.last_check_in = now
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'打卡成功！当前连续{habit.current_streak}天',
        'streak': habit.current_streak
    })

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/sw.js')
def serve_worker():
    return send_from_directory('static', 'sw.js')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

# Vercel 需要的 WSGI 应用
app = app
