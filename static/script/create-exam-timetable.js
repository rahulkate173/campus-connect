document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('examForm');
    const list = document.getElementById('timetableList');

    const renderSlot = (data) => {
        const div = document.createElement('div');
        div.className = 'slot-card';
        div.innerHTML = `
            <div class="slot-info">
                <h4>${data.subject}</h4>
                <p><i class="far fa-calendar-alt"></i> ${data.date} | <i class="far fa-clock"></i> ${data.time}</p>
            </div>
            <div class="slot-meta" style="display:flex; align-items:center; gap:20px;">
                <span class="room-badge">${data.room}</span>
                <button class="remove-btn"><i class="fas fa-trash-alt"></i></button>
            </div>
        `;
        list.prepend(div);
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const newSlot = {
            date: document.getElementById('examDate').value,
            subject: document.getElementById('examSubject').value,
            time: document.getElementById('examTime').value,
            room: document.getElementById('examRoom').value
        };
        renderSlot(newSlot);
        form.reset();
    });

    list.addEventListener('click', (e) => {
        if (e.target.closest('.remove-btn')) {
            e.target.closest('.slot-card').remove();
        }
    });
});