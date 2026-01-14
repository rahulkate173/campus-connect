const notices = [
    {
        type: 'exam',
        title: 'Mid-Semester Timetable Released',
        date: { day: '18', month: 'Jan' },
        desc: 'The timetable for Mid-Sem Examination is now available. Exams begin next Monday.'
    },
    {
        type: 'college',
        title: 'Annual Cultural Fest: ZEST 2026',
        date: { day: '22', month: 'Jan' },
        desc: 'We are excited to announce our annual fest. Registration for events is now open.'
    },
    {
        type: 'exam',
        title: 'Remedial Exam Form Deadline',
        date: { day: '15', month: 'Jan' },
        desc: 'Last date to submit remedial exam forms for Sem III is tomorrow by 4 PM.'
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const feed = document.getElementById('announcementFeed');
    const buttons = document.querySelectorAll('.tab-btn');

    const render = (filter = 'all') => {
        feed.innerHTML = '';
        const filtered = filter === 'all' ? notices : notices.filter(n => n.type === filter);
        
        filtered.forEach(n => {
            const card = document.createElement('div');
            card.className = `ann-card ${n.type}`;
            card.innerHTML = `
                <div class="date-badge">
                    <span class="day">${n.date.day}</span>
                    <span class="month">${n.date.month}</span>
                </div>
                <div class="content-box">
                    <span class="tag">${n.type === 'exam' ? 'Examination' : 'Campus News'}</span>
                    <h3>${n.title}</h3>
                    <p>${n.desc}</p>
                </div>
            `;
            feed.appendChild(card);
        });
    };

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            render(btn.dataset.filter);
        });
    });

    render(); // Initial Load
});