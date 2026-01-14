const students = [
    { id: 1, name: "Arjun Mehta" },
    { id: 2, name: "Sanya Iyer" },
    { id: 3, name: "Rohan Das" }
];

document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('marksTableBody');

    // Generate rows
    tableBody.innerHTML = students.map((st, index) => `
        <tr data-id="${st.id}">
            <td>${index + 1}</td>
            <td><strong>${st.name}</strong></td>
            <td><input type="number" class="mark-input ut" max="15" value="0"></td>
            <td><input type="number" class="mark-input lab" max="10" value="0"></td>
            <td><input type="number" class="mark-input att" max="5" value="0"></td>
            <td class="total-cell">0</td>
        </tr>
    `).join('');

    // Auto-calculate Total when marks change
    tableBody.addEventListener('input', (e) => {
        if (e.target.classList.contains('mark-input')) {
            const row = e.target.closest('tr');
            const ut = parseFloat(row.querySelector('.ut').value) || 0;
            const lab = parseFloat(row.querySelector('.lab').value) || 0;
            const att = parseFloat(row.querySelector('.att').value) || 0;
            
            row.querySelector('.total-cell').textContent = ut + lab + att;
        }
    });
});