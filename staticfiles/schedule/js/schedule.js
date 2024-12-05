document.addEventListener('DOMContentLoaded', function() {
    const schedulesContainer = document.getElementById('schedules-container');
    const addScheduleBtn = document.getElementById('add-schedule');
    const calendarEl = document.getElementById('calendar');
    let calendar;

    // Initialize FullCalendar
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        slotMinTime: '08:00:00',
        slotMaxTime: '20:00:00',
        allDaySlot: false,
        events: [],
        editable: false,
    });
    calendar.render();

    // Function to update calendar events
    function updateCalendarEvents() {
        calendar.removeAllEvents();
        const schedulesForms = document.querySelectorAll('.schedule-form');
        
        schedulesForms.forEach(form => {
            const startDate = form.querySelector('[name="start_date"]').value;
            const endDate = form.querySelector('[name="end_date"]').value;
            const startTime = form.querySelector('[name="start_time"]').value;
            const endTime = form.querySelector('[name="end_time"]').value;
            const selectedDays = Array.from(form.querySelectorAll('.schedule-day-checkbox:checked'))
                .map(checkbox => checkbox.value);
            
            if (startDate && endDate && startTime && endTime && selectedDays.length > 0) {
                const events = generateRecurringEvents(
                    startDate,
                    endDate,
                    startTime,
                    endTime,
                    selectedDays
                );
                events.forEach(event => calendar.addEvent(event));
            }
        });
    }

    // Function to generate recurring events
    function generateRecurringEvents(startDate, endDate, startTime, endTime, days) {
        const events = [];
        const start = new Date(startDate);
        const end = new Date(endDate);
        const dayMap = {
            'M': 1, 'T': 2, 'W': 3, 'H': 4, 'F': 5, 'S': 6, 'S': 0
        };

        while (start <= end) {
            if (days.includes(Object.keys(dayMap).find(key => dayMap[key] === start.getDay()))) {
                events.push({
                    title: 'Course Session',
                    start: `${start.toISOString().split('T')[0]}T${startTime}`,
                    end: `${start.toISOString().split('T')[0]}T${endTime}`,
                    backgroundColor: '#3B82F6',
                });
            }
            start.setDate(start.getDate() + 1);
        }
        return events;
    }

    // Add event listeners for form changes
    schedulesContainer.addEventListener('change', updateCalendarEvents);
    
    // Add Schedule button functionality
    addScheduleBtn.addEventListener('click', function() {
        const template = document.querySelector('.schedule-form').cloneNode(true);
        template.querySelectorAll('input').forEach(input => input.value = '');
        template.querySelectorAll('.schedule-day-checkbox').forEach(checkbox => checkbox.checked = false);
        schedulesContainer.appendChild(template);
    });

    // Remove Schedule button functionality
    schedulesContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-schedule')) {
            const scheduleForm = e.target.closest('.schedule-form');
            if (document.querySelectorAll('.schedule-form').length > 1) {
                scheduleForm.remove();
                updateCalendarEvents();
            }
        }
    });

    // Initialize tooltips for schedule day checkboxes
    const dayTooltips = {
        'M': 'Monday',
        'T': 'Tuesday',
        'W': 'Wednesday',
        'H': 'Thursday',
        'F': 'Friday',
        'S': 'Saturday',
        'S': 'Sunday'
    };

    document.querySelectorAll('.schedule-day-checkbox').forEach(checkbox => {
        const day = checkbox.value;
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = dayTooltips[day];
        checkbox.parentElement.appendChild(tooltip);
    });
});

