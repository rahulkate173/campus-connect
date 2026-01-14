document.addEventListener('DOMContentLoaded', () => {
    const createBtn = document.getElementById('openModal');

    createBtn.addEventListener('click', () => {
        // This would open a modal or navigate to a builder page
        alert("Redirecting to Quiz Builder...");
        // window.location.href = 'quiz-builder.html';
    });

    const monitorBtns = document.querySelectorAll('.monitor-btn');
    monitorBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            alert("Opening Live Proctoring Feed...");
        });
    });
});