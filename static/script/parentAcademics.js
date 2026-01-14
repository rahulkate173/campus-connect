import { supabase } from './supabase-config.js';

document.addEventListener('DOMContentLoaded', async () => {
    // Containers for dynamic content
    const internalList = document.querySelector('.internal-list');
    const annList = document.querySelector('.announcement-list');

    /**
     * 1. RENDER INTERNAL MARKS
     * Loops through subject data and calculates bar colors
     */
    const renderInternalMarks = (marks) => {
        internalList.innerHTML = ''; // Clear loader

        marks.forEach(item => {
            const percentage = (item.obtained / item.total) * 100;
            let statusClass = '';

            // Logic: Color coding for parent's quick view
            if (percentage < 50) statusClass = 'danger';
            else if (percentage < 75) statusClass = 'warning';

            const row = document.createElement('div');
            row.className = 'subject-row';
            row.innerHTML = `
                <span>${item.subject}</span>
                <div class="progress-container">
                    <div class="progress-bar ${statusClass}" style="width: ${percentage}%;"></div>
                    <span class="mark-text">${item.obtained} / ${item.total}</span>
                </div>
            `;
            internalList.appendChild(row);
        });
    };

    /**
     * 2. FETCH DATA FROM SUPABASE
     * Assuming you have a 'marks' table and an 'announcements' table
     */
    const fetchData = async () => {
        try {
            // Get Internal Marks (Filtered by Student ID)
            // Replace 'student_123' with the actual ID from your auth session
            const { data: marks, error: mError } = await supabase
                .from('internal_marks')
                .select('*')
                .eq('student_id', 'student_123');

            if (marks) renderInternalMarks(marks);

            // Get Exam Announcements
            const { data: ann, error: aError } = await supabase
                .from('announcements')
                .select('*')
                .eq('category', 'exam')
                .order('created_at', { ascending: false });

            // If you have announcement data, you would render it here similarly
        } catch (err) {
            console.error("Error fetching academic data:", err);
        }
    };

    // Initialize the fetch
    fetchData();

    // MOCK DATA: For testing the Frontend before Backend is ready
    const mockMarks = [
        { subject: 'Operating Systems', obtained: 27, total: 30 },
        { subject: 'Database Management', obtained: 24, total: 30 },
        { subject: 'Mathematics IV', obtained: 14, total: 30 } // This will trigger the red/orange bar
    ];
    
    // Uncomment the line below to test the UI without Supabase
    // renderInternalMarks(mockMarks);
});