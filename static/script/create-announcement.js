import { supabase } from './supabase-config.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('announcementForm');
    const historyContainer = document.getElementById('announcementHistory');

    const renderHistory = (announcements) => {
        historyContainer.innerHTML = announcements.map(ann => `
            <div class="history-card ${ann.priority === 'urgent' ? 'urgent' : ''}">
                <div class="msg-content">
                    <h4>To: ${ann.target}</h4>
                    <p>${ann.content}</p>
                </div>
                <div class="msg-date">${ann.date}</div>
            </div>
        `).join('');
    };

    // Dummy data to show frontend works
    const dummyData = [
        { target: 'TE Div A', content: 'The lecture scheduled for 2 PM is cancelled.', priority: 'urgent', date: 'Jan 14, 10:30 AM' },
        { target: 'All Students', content: 'Please submit your journals by Friday.', priority: 'normal', date: 'Jan 13, 04:15 PM' }
    ];

    renderHistory(dummyData);

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = document.getElementById('messageContent').value;
        const target = document.getElementById('targetClass').value;
        const priority = document.getElementById('priority').value;

        // In the future, use Supabase here:
        // await supabase.from('announcements').insert([{ content, target, priority }]);
        
        alert(`Announcement posted to ${target}!`);
        form.reset();
    });
});