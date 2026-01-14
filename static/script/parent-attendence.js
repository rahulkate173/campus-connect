const attendanceData = [
    { subject: "Operating Systems", attended: 38, total: 40 },
    { subject: "Database Systems", attended: 32, total: 40 },
    { subject: "Mathematics IV", attended: 22, total: 35 }, // 62% - Alert
    { subject: "Computer Networks", attended: 25, total: 40 } // 62.5% - Alert
];

document.addEventListener('DOMContentLoaded', () => {
    const alertContainer = document.getElementById('alertContainer');
    const grid = document.getElementById('subjectGrid');

    alertContainer.innerHTML = ''; // Clear hardcoded HTML

    attendanceData.forEach(item => {
        const percentage = Math.round((item.attended / item.total) * 100);
        
        // 1. Render all subjects in the grid
        const miniCard = document.createElement('div');
        miniCard.className = 'subject-mini-card';
        miniCard.innerHTML = `
            <span class="sub-name">${item.subject}</span>
            <span class="sub-per ${percentage < 75 ? 'low' : ''}">${percentage}%</span>
        `;
        grid.appendChild(miniCard);

        // 2. If attendance is low, push to alerts section
        if (percentage < 75) {
            const alert = document.createElement('div');
            alert.className = 'alert-item';
            alert.innerHTML = `
                <div class="alert-icon"><i class="fas fa-exclamation-circle"></i></div>
                <div class="alert-text">
                    <h4>${item.subject} Alert</h4>
                    <p>Current: <strong>${percentage}%</strong>. This is below the required 75% threshold.</p>
                </div>
                <button class="notify-btn">Details</button>
            `;
            alertContainer.appendChild(alert);
        }
    });
});