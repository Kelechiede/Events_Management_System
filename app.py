#####################################################
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:POSTgres123%40@localhost/ems_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%dT%H:%M'):
    return value.strftime(format)

class User(UserMixin, db.Model): 
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True) # autoincrement=True
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='user', passive_deletes=True)
    attendees = db.relationship('Attendee', backref='attendee_user', passive_deletes=True)

    def get_id(self):
        return self.user_id

class Venue(db.Model):
    __tablename__ = 'venues'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='venue', passive_deletes=True)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True) #autoincrement=True
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attendees = db.relationship('Attendee', backref='event', passive_deletes=True)

class Attendee(db.Model):
    __tablename__ = 'attendees'
    attendee_id = db.Column(db.Integer, primary_key=True) # autoincrement=True
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    with Session(db.engine) as session:
        return session.get(User, int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Signup successful! You are now logged in.', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/register_event/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not Attendee.query.filter_by(user_id=current_user.user_id, event_id=event.event_id).first():
        attendee = Attendee(user_id=current_user.user_id, event_id=event.event_id)
        db.session.add(attendee)
        db.session.commit()
        flash('You have successfully registered for the event.', 'success')
    else:
        flash('You are already registered for this event.', 'info')
    return redirect(url_for('events'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/venues')
@login_required
def venues():
    venues = Venue.query.all()
    return render_template('venues.html', venues=venues)

@app.route('/add_venue', methods=['GET', 'POST'])
@login_required
def add_venue():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        capacity = request.form['capacity']
        new_venue = Venue(name=name, location=location, capacity=capacity)
        try:
            db.session.add(new_venue)
            db.session.commit()
            flash('Venue added successfully!', 'success')
            return redirect(url_for('venues'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e.orig), 'danger')
    return render_template('add_venue.html')

@app.route('/update_venue/<int:venue_id>', methods=['GET', 'POST'])
@login_required
def update_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if request.method == 'POST':
        venue.name = request.form['name']
        venue.location = request.form['location']
        venue.capacity = request.form['capacity']
        db.session.commit()
        flash('Venue updated successfully!', 'success')
        return redirect(url_for('venues'))
    return render_template('update_venue.html', venue=venue)

@app.route('/delete_venue/<int:venue_id>', methods=['POST'])
@login_required
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted successfully!', 'success')
    return redirect(url_for('venues'))

@app.route('/events')
@login_required
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        user_id = request.form['user_id']
        venue_id = request.form['venue_id']
        title = request.form['title']
        description = request.form['description']
        event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%dT%H:%M')
        new_event = Event(user_id=user_id, venue_id=venue_id, title=title, description=description, event_date=event_date)
        try:
            db.session.add(new_event)
            db.session.commit()
            flash('Event added successfully!', 'success')
            return redirect(url_for('events'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e.orig), 'danger')
    users = User.query.all()
    venues = Venue.query.all()
    return render_template('add_event.html', users=users, venues=venues)

@app.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.user_id = request.form['user_id']
        event.venue_id = request.form['venue_id']
        event.title = request.form['title']
        event.description = request.form['description']
        event.event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%dT%H:%M')
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events'))
    users = User.query.all()
    venues = Venue.query.all()
    return render_template('update_event.html', event=event, users=users, venues=venues)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        # Delete all attendees related to the event first
        Attendee.query.filter_by(event_id=event_id).delete()
        db.session.delete(event)
        db.session.commit()
        flash('Event and associated attendees deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error: ' + str(e), 'danger')
    return redirect(url_for('events'))

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully!', 'success')
            return redirect(url_for('users'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e.orig), 'danger')
    return render_template('add_user.html')

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))

@app.route('/visualizations')
@login_required
def visualizations():
    return render_template('visualizations.html')

@app.route('/api/user_registration_trends')
def api_user_registration_trends():
    user_registration_trends = db.session.query(db.func.date_trunc('month', User.created_at).label('month'), db.func.count(User.user_id)).group_by('month').order_by('month').all()
    data = {
        "labels": [month.strftime('%Y-%m') for month, _ in user_registration_trends],
        "values": [count for _, count in user_registration_trends]
    }
    return jsonify(data)

@app.route('/api/event_popularity')
def api_event_popularity():
    event_popularity = db.session.query(Event.title, db.func.count(Attendee.attendee_id)).join(Attendee).group_by(Event.title).order_by(db.func.count(Attendee.attendee_id).desc()).all()
    data = {
        "labels": [title for title, _ in event_popularity],
        "values": [count for _, count in event_popularity]
    }
    return jsonify(data)

@app.route('/api/events_per_venue')
def api_events_per_venue():
    events_per_venue = db.session.query(Venue.name, db.func.count(Event.event_id)).join(Event).group_by(Venue.name).all()
    data = {
        "labels": [name for name, _ in events_per_venue],
        "values": [count for _, count in events_per_venue]
    }
    return jsonify(data)

@app.route('/api/attendees_per_event')
def api_attendees_per_event():
    attendees_per_event = db.session.query(Event.title, db.func.count(Attendee.attendee_id)).join(Attendee).group_by(Event.title).all()
    data = {
        "labels": [title for title, _ in attendees_per_event],
        "values": [count for _, count in attendees_per_event]
    }
    return jsonify(data)

@app.route('/api/event_dates_distribution')
def api_event_dates_distribution():
    event_dates_distribution = db.session.query(db.func.date(Event.event_date).label('date'), db.func.count(Event.event_id)).group_by('date').order_by('date').all()
    data = {
        "labels": [date.strftime('%Y-%m-%d') for date, _ in event_dates_distribution],
        "values": [count for _, count in event_dates_distribution]
    }
    return jsonify(data)

@app.route('/api/events_per_user')
def api_events_per_user():
    events_per_user = db.session.query(User.username, db.func.count(Event.event_id)).join(Event).group_by(User.username).order_by(User.username).all()
    data = {
        "labels": [username for username, _ in events_per_user],
        "values": [count for _, count in events_per_user]
    }
    return jsonify(data)

@app.route('/api/average_attendees')
def api_average_attendees():
    subquery = db.session.query(Event.event_id, db.func.count(Attendee.attendee_id).label('attendee_count')).join(Attendee).group_by(Event.event_id).subquery()
    average_attendees = db.session.query(db.func.avg(subquery.c.attendee_count)).scalar()
    data = {
        "value": round(average_attendees, 2)
    }
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False) # Set debug to False for production
