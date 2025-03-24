from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for
from models.models import db, Event
from flask_login import login_required, current_user

event_bp = Blueprint('events', __name__)

@event_bp.route('/')
@event_bp.route('/list')
@login_required
def event_list():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('event_list.html', events=events)

@event_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_event():
    today_date = date.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
    if request.method == 'POST':
        event_date = request.form['date']

        # Prevent past dates from being saved
        if event_date < today_date:
            return render_template('add_event.html', error="Event date cannot be in the past!", today_date=today_date)

        new_event = Event(
            title=request.form['title'],
            description=request.form['description'],
            date=event_date,
            time=request.form['time'],
            location=request.form['location'],
            user_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('events.event_list'))

    return render_template('add_event.html', today_date=today_date)

@event_bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get(event_id)

    if not event or event.user_id != current_user.id:
        return redirect(url_for('events.event_list'))

    today_date = date.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format

    if request.method == 'POST':
        event_date = request.form['date']

        # Prevent past dates from being updated
        if event_date < today_date:
            return render_template('edit_event.html', event=event, error="Event date cannot be in the past!", today_date=today_date)

        event.title = request.form['title']
        event.description = request.form['description']
        event.date = event_date
        event.time = request.form['time']
        event.location = request.form['location']
        db.session.commit()
        return redirect(url_for('events.event_list'))

    return render_template('edit_event.html', event=event, today_date=today_date)

@event_bp.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event and event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('events.event_list'))
