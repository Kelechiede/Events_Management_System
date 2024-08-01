document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/events_per_venue')
        .then(response => response.json())
        .then(data => createChart('eventsPerVenueChart', 'bar', data.labels, data.values, 'Events per Venue'));

    fetch('/api/attendees_per_event')
        .then(response => response.json())
        .then(data => createChart('attendeesPerEventChart', 'bar', data.labels, data.values, 'Attendees per Event'));

    fetch('/api/user_registration_trends')
        .then(response => response.json())
        .then(data => createChart('userRegistrationTrendsChart', 'line', data.labels, data.values, 'User Registration Trends'));

    fetch('/api/event_popularity')
        .then(response => response.json())
        .then(data => createChart('eventPopularityChart', 'bar', data.labels, data.values, 'Event Popularity'));

    fetch('/api/event_dates_distribution')
        .then(response => response.json())
        .then(data => createChart('eventDatesDistributionChart', 'bar', data.labels, data.values, 'Event Dates Distribution'));

    fetch('/api/events_per_user')
        .then(response => response.json())
        .then(data => {
            createChart('eventsPerUserChart', 'bar', data.labels, data.values, 'Events per User');
            createChart('eventsPerUserPieChart', 'pie', data.labels, data.values, 'Percentage of Events per User');
        });

    fetch('/api/events_per_venue')
        .then(response => response.json())
        .then(data => createChart('eventsPerVenuePieChart', 'pie', data.labels, data.values, 'Percentage of Events per Venue'));

    fetch('/api/average_attendees')
        .then(response => response.json())
        .then(data => {
            const avgAttendeesDiv = document.getElementById('averageAttendees');
            avgAttendeesDiv.innerHTML = `<h3>Average Attendees per Event: ${data.value}</h3>`;
        });

    function createChart(elementId, chartType, labels, data, title) {
        new Chart(document.getElementById(elementId), {
            type: chartType,
            data: {
                labels: labels,
                datasets: [{
                    label: title,
                    data: data,
                    backgroundColor: chartType === 'pie' ? generateColors(data.length) : 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: chartType === 'pie' ? 'right' : 'top',
                    },
                    title: {
                        display: true,
                        text: title
                    }
                }
            }
        });
    }

    function generateColors(numColors) {
        const colors = [];
        for (let i = 0; i < numColors; i++) {
            colors.push(`hsl(${i * 360 / numColors}, 100%, 75%)`);
        }
        return colors;
    }
});
