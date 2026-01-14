document.addEventListener('DOMContentLoaded', () => {
    const dayBtns = document.querySelectorAll('.day-btn');

    dayBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // UI Toggle
            dayBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const selectedDay = btn.getAttribute('data-day');
            console.log("Fetching timetable for:", selectedDay);
            
            // Here you would fetch from Supabase based on the day
            // fetchTimetable(selectedDay); 
        });
    });
});