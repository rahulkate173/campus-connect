// Sample Data - In real app, this comes from Supabase
const students = [
    { id: 101, name: "Arjun Mehta" },
    { id: 102, name: "Sanya Iyer" },
    { id: 103, name: "Rohan Das" },
    { id: 104, name: "Priya Patil" }
];

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('studentContainer');
    const form = document.getElementById('attendanceForm');

    // 1. DYNAMICALLY GENERATE THE LIST
    container.innerHTML = students.map((student, index) => `
        <div class="student-row">
            <div class="student-info">
                <span class="roll-no">${index + 1}</span>
                <span class="student-name">${student.name}</span>
            </div>
            <div class="status-group">
                <input type="radio" name="attendance-${student.id}" id="p-${student.id}" value="P" checked>
                <label for="p-${student.id}" class="status-label">P</label>
                
                <input type="radio" name="attendance-${student.id}" id="a-${student.id}" value="A">
                <label for="a-${student.id}" class="status-label">A</label>
            </div>
        </div>
    `).join('');

    // 2. MARK ALL PRESENT BUTTON
    document.getElementById('markAllPresent').addEventListener('click', (e) => {
        e.preventDefault();
        const presentRadios = document.querySelectorAll('input[value="P"]');
        presentRadios.forEach(radio => radio.checked = true);
    });

    // 3. HANDLE FORM SUBMISSION
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        console.log("Attendance Data to send to Backend:", Object.fromEntries(formData));
        alert("Attendance Data Saved Successfully!");
    });
});