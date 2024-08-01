import sys
import os

# Ensure the parent directory is in the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User, Venue, Event, Attendee
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def create_sample_data():
    app = create_app()
    with app.app_context():
        # Create users with different registration dates
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'date': datetime(2024, 1, 1)},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'date': datetime(2024, 2, 1)},
            {'username': 'alice_wonder', 'email': 'alice@example.com', 'date': datetime(2024, 3, 1)},
            {'username': 'bob_builder', 'email': 'bob@example.com', 'date': datetime(2024, 4, 1)},
            {'username': 'mike_tyson', 'email': 'mike@example.com', 'date': datetime(2024, 5, 1)},
            {'username': 'susan_clark', 'email': 'susan@example.com', 'date': datetime(2024, 6, 1)},
            {'username': 'david_lee', 'email': 'david@example.com', 'date': datetime(2024, 7, 1)},
            {'username': 'emma_brown', 'email': 'emma@example.com', 'date': datetime(2024, 8, 1)},
            {'username': 'noah_white', 'email': 'noah@example.com', 'date': datetime(2024, 9, 1)},
            {'username': 'olivia_green', 'email': 'olivia@example.com', 'date': datetime(2024, 10, 1)},
            {'username': 'liam_black', 'email': 'liam@example.com', 'date': datetime(2024, 11, 1)},
            {'username': 'ava_blue', 'email': 'ava@example.com', 'date': datetime(2024, 12, 1)}
        ]

        users = []
        for user_data in users_data:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(
                    username=user_data['username'],
                    password_hash=generate_password_hash('password123', method='pbkdf2:sha256'),
                    email=user_data['email'],
                    created_at=user_data['date']
                )
                users.append(user)

        if users:
            db.session.add_all(users)
            db.session.commit()

        # Retrieve user IDs
        user_ids = {user.username: user.user_id for user in User.query.all()}

        # Create venues
        venue_names = ['Expo Center', 'Outdoor Arena', 'Tech Park', 'Convention Hall']
        venues = [
            Venue(name='Expo Center', location='456 Expo Drive', capacity=1000),
            Venue(name='Outdoor Arena', location='789 Arena Road', capacity=3000),
            Venue(name='Tech Park', location='123 Tech Lane', capacity=800),
            Venue(name='Convention Hall', location='321 Convention Blvd', capacity=1200)
        ]

        existing_venues = {venue.name: venue for venue in Venue.query.filter(Venue.name.in_(venue_names)).all()}
        new_venues = [venue for venue in venues if venue.name not in existing_venues]

        if new_venues:
            db.session.add_all(new_venues)
            db.session.commit()

        # Retrieve venue IDs
        venue_ids = {venue.name: venue.venue_id for venue in Venue.query.filter(Venue.name.in_(venue_names)).all()}

        # Create events
        event_titles = ['Music Festival', 'Food Carnival', 'Tech Expo', 'Art Exhibition', 'Business Conference', 'Startup Pitch', 'Health Workshop', 'Gaming Convention']
        events = [
            Event(user_id=user_ids['john_doe'], venue_id=venue_ids['Expo Center'], title='Music Festival', description='A grand music festival.', event_date=datetime(2024, 5, 20, 18, 0)),
            Event(user_id=user_ids['jane_smith'], venue_id=venue_ids['Outdoor Arena'], title='Food Carnival', description='A carnival with diverse food stalls.', event_date=datetime(2024, 6, 15, 12, 0)),
            Event(user_id=user_ids['alice_wonder'], venue_id=venue_ids['Tech Park'], title='Tech Expo', description='An exhibition of the latest tech.', event_date=datetime(2024, 7, 10, 10, 0)),
            Event(user_id=user_ids['bob_builder'], venue_id=venue_ids['Convention Hall'], title='Art Exhibition', description='Showcasing modern art.', event_date=datetime(2024, 8, 5, 9, 0)),
            Event(user_id=user_ids['mike_tyson'], venue_id=venue_ids['Expo Center'], title='Business Conference', description='A conference for business professionals.', event_date=datetime(2024, 9, 12, 9, 0)),
            Event(user_id=user_ids['susan_clark'], venue_id=venue_ids['Outdoor Arena'], title='Startup Pitch', description='Pitching event for startups.', event_date=datetime(2024, 10, 20, 14, 0)),
            Event(user_id=user_ids['david_lee'], venue_id=venue_ids['Tech Park'], title='Health Workshop', description='A workshop on health and wellness.', event_date=datetime(2024, 11, 22, 11, 0)),
            Event(user_id=user_ids['emma_brown'], venue_id=venue_ids['Convention Hall'], title='Gaming Convention', description='A convention for gaming enthusiasts.', event_date=datetime(2024, 12, 5, 10, 0))
        ]

        existing_events = {event.title: event for event in Event.query.filter(Event.title.in_(event_titles)).all()}
        new_events = [event for event in events if event.title not in existing_events]

        if new_events:
            db.session.add_all(new_events)
            db.session.commit()

        # Retrieve event IDs
        event_ids = {event.title: event.event_id for event in Event.query.filter(Event.title.in_(event_titles)).all()}

        # Create attendees
        attendees = [
            Attendee(user_id=user_ids['jane_smith'], event_id=event_ids['Music Festival']),
            Attendee(user_id=user_ids['alice_wonder'], event_id=event_ids['Music Festival']),
            Attendee(user_id=user_ids['bob_builder'], event_id=event_ids['Food Carnival']),
            Attendee(user_id=user_ids['mike_tyson'], event_id=event_ids['Food Carnival']),
            Attendee(user_id=user_ids['susan_clark'], event_id=event_ids['Tech Expo']),
            Attendee(user_id=user_ids['david_lee'], event_id=event_ids['Tech Expo']),
            Attendee(user_id=user_ids['john_doe'], event_id=event_ids['Art Exhibition']),
            Attendee(user_id=user_ids['jane_smith'], event_id=event_ids['Art Exhibition']),
            Attendee(user_id=user_ids['alice_wonder'], event_id=event_ids['Business Conference']),
            Attendee(user_id=user_ids['bob_builder'], event_id=event_ids['Business Conference']),
            Attendee(user_id=user_ids['mike_tyson'], event_id=event_ids['Startup Pitch']),
            Attendee(user_id=user_ids['susan_clark'], event_id=event_ids['Startup Pitch']),
            Attendee(user_id=user_ids['david_lee'], event_id=event_ids['Health Workshop']),
            Attendee(user_id=user_ids['emma_brown'], event_id=event_ids['Health Workshop']),
            Attendee(user_id=user_ids['noah_white'], event_id=event_ids['Gaming Convention']),
            Attendee(user_id=user_ids['olivia_green'], event_id=event_ids['Gaming Convention'])
        ]

        db.session.add_all(attendees)
        db.session.commit()

        print("Sample data created successfully.")

if __name__ == '__main__':
    create_sample_data()
