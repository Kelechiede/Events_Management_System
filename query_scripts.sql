-- select * from attendee;

select * from attendees;

select * from venues;

select * from events;

select * from users;


SELECT setval('venues_venue_id_seq', (SELECT MAX(venue_id) FROM venues));

SELECT setval('attendees_attendee_id_seq', (SELECT MAX(attendee_id) FROM attendees));

SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));


SELECT setval('events_event_id_seq', (SELECT MAX(event_id) FROM events));


