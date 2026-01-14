import { supabase } from './supabase-config.js';

document.addEventListener('DOMContentLoaded', () => {
   
    const container = document.getElementById('studentListContainer');

   
    const renderStudents = (students) => {
       

        students.forEach((student, index) => {
            const row = document.createElement('div');
            row.className = 'student-row';
            
           
            const pId = `p-${student.id}`;
            const aId = `a-${student.id}`;

            row.innerHTML = `
                <div class="st-info">
                    <span class="roll">${index + 1}</span>
                    <span class="name">${student.full_name}</span>
                </div>
                <div class="status-toggle">
                    <input type="radio" name="${student.id}" id="${pId}" value="P" checked>
                    <label for="${pId}" class="p-label">P</label>
                    
                    <input type="radio" name="${student.id}" id="${aId}" value="A">
                    <label for="${aId}" class="a-label">A</label>
                </div>
            `;
            container.appendChild(row);
        });
    };

    // 3. FETCH DATA FROM SUPABASE (Frontend-Backend Connection)
    const fetchStudents = async () => {
        try {
            // Replace 'profiles' with your actual table name
            const { data, error } = await supabase
                .from('profiles')
                .select('id, full_name')
                .eq('role', 'student')
                .order('full_name', { ascending: true });

            if (error) throw error;
            
            if (data) {
                renderStudents(data);
            }
        } catch (error) {
            console.error("Error fetching students:", error.message);
            container.innerHTML = `<p style="color:red; padding:20px;">Failed to load students.</p>`;
        }
    };

    // Initialize
    fetchStudents();

    // Select All Button Logic
    document.getElementById('markAllPresent').addEventListener('click', (e) => {
        e.preventDefault();
        const allPresentRadios = document.querySelectorAll('input[value="P"]');
        allPresentRadios.forEach(radio => radio.checked = true);
    });
});