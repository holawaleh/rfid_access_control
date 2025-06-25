from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, RFIDCard, AccessLog, Door
from forms import LoginForm, RegisterForm, RFIDCardForm, DoorForm
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        recent_logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).limit(10).all()
        total_cards = RFIDCard.query.count()
        active_cards = RFIDCard.query.filter_by(is_active=True).count()
        total_doors = Door.query.count()
        return render_template('dashboard.html', 
                             recent_logs=recent_logs,
                             total_cards=total_cards,
                             active_cards=active_cards,
                             total_doors=total_doors)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cards')
@login_required
def cards():
    cards = RFIDCard.query.all()
    return render_template('cards.html', cards=cards)

@app.route('/cards/add', methods=['GET', 'POST'])
@login_required
def add_card():
    form = RFIDCardForm()
    users = User.query.all()
    form.user_id.choices = [(0, 'Unassigned')] + [(u.id, u.username) for u in users]
    
    if form.validate_on_submit():
        card = RFIDCard(
            card_uid=form.card_uid.data,
            user_id=form.user_id.data if form.user_id.data != 0 else None,
            description=form.description.data,
            is_active=form.is_active.data
        )
        db.session.add(card)
        db.session.commit()
        flash('RFID card added successfully')
        return redirect(url_for('cards'))
    return render_template('add_card.html', form=form)

@app.route('/cards/<int:card_id>/toggle')
@login_required
def toggle_card(card_id):
    card = RFIDCard.query.get_or_404(card_id)
    card.is_active = not card.is_active
    db.session.commit()
    flash(f'Card {"activated" if card.is_active else "deactivated"}')
    return redirect(url_for('cards'))

@app.route('/logs')
@login_required
def logs():
    page = request.args.get('page', 1, type=int)
    logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('logs.html', logs=logs)

@app.route('/doors')
@login_required
def doors():
    doors = Door.query.all()
    return render_template('doors.html', doors=doors)

@app.route('/doors/add', methods=['GET', 'POST'])
@login_required
def add_door():
    form = DoorForm()
    if form.validate_on_submit():
        door = Door(name=form.name.data, location=form.location.data)
        db.session.add(door)
        db.session.commit()
        flash('Door added successfully')
        return redirect(url_for('doors'))
    return render_template('add_door.html', form=form)

@app.route('/doors/<int:door_id>/toggle')
@login_required
def toggle_door(door_id):
    door = Door.query.get_or_404(door_id)
    door.is_locked = not door.is_locked
    door.last_accessed = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'success', 'locked': door.is_locked})

# API endpoint for RFID scanner
@app.route('/api/access', methods=['POST'])
def check_access():
    data = request.get_json()
    card_uid = data.get('card_uid')
    door_id = data.get('door_id', 1)
    
    if not card_uid:
        return jsonify({'access_granted': False, 'message': 'No card UID provided'})
    
    card = RFIDCard.query.filter_by(card_uid=card_uid).first()
    access_granted = card is not None and card.is_active
    
    # Log the access attempt
    log = AccessLog(
        card_uid=card_uid,
        access_granted=access_granted,
        user_id=card.user_id if card else None
    )
    db.session.add(log)
    
    if access_granted:
        card.last_used = datetime.utcnow()
        door = Door.query.get(door_id)
        if door:
            door.last_accessed = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'access_granted': access_granted,
        'message': 'Access granted' if access_granted else 'Access denied',
        'user': card.user.username if card and card.user else None
    })

@app.before_first_request
def create_tables():
    db.create_all()
    
    # Create default admin user if none exists
    if not User.query.filter_by(is_admin=True).first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)