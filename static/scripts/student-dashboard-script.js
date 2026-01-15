/**
 * Student Dashboard Script
 * Loads and displays student data on the dashboard
 */

// Get student ID from session or local storage
// In production, this would come from the authenticated session
const getStudentId = () => {
    // This is a placeholder - in production, get from session
    return localStorage.getItem('studentId') || 'STUDENT_ID';
};

// Load dashboard data when page loads
document.addEventListener('DOMContentLoaded', async () => {
    const studentId = getStudentId();

    try {
        // Load student profile
        await loadStudentProfile(studentId);

        // Load attendance data
        await loadAttendanceData(studentId);

        // Load announcements
        await loadAnnouncements();

        // Load marks/results
        await loadMarksData(studentId);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
});

/**
 * Load student profile information
 */
async function loadStudentProfile(studentId) {
    try {
        const result = await API.Profile.getProfile(studentId);
        
        if (result.success && result.data) {
            const profile = result.data;
            
            // Update profile elements on page
            const nameElement = document.getElementById('studentName');
            const classElement = document.getElementById('studentClass');
            const emailElement = document.getElementById('studentEmail');
            
            if (nameElement) nameElement.textContent = profile.name || 'Student';
            if (classElement) classElement.textContent = profile.class_year || 'N/A';
            if (emailElement) emailElement.textContent = profile.email || 'N/A';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

/**
 * Load attendance data
 */
async function loadAttendanceData(studentId) {
    try {
        const result = await API.Attendance.getStudentAttendance(studentId);
        
        if (result.success) {
            const attendanceElement = document.getElementById('attendancePercentage');
            const totalElement = document.getElementById('totalClasses');
            
            if (attendanceElement) {
                attendanceElement.textContent = result.overall_percentage.toFixed(1) + '%';
            }
            if (totalElement) {
                totalElement.textContent = result.total_records || 0;
            }
        }
    } catch (error) {
        console.error('Error loading attendance:', error);
    }
}

/**
 * Load announcements
 */
async function loadAnnouncements() {
    try {
        const result = await API.Announcement.getAnnouncements('student');
        
        if (result.success && result.data) {
            const announcementsList = document.getElementById('announcementsList');
            
            if (announcementsList) {
                announcementsList.innerHTML = '';
                
                if (result.data.length === 0) {
                    announcementsList.innerHTML = '<p>No announcements available.</p>';
                    return;
                }
                
                result.data.forEach(announcement => {
                    const announcementDiv = document.createElement('div');
                    announcementDiv.className = 'announcement-item';
                    announcementDiv.innerHTML = `
                        <h4>${announcement.title || 'Announcement'}</h4>
                        <p>${announcement.content || ''}</p>
                        <small>${new Date(announcement.created_at).toLocaleDateString()}</small>
                    `;
                    announcementsList.appendChild(announcementDiv);
                });
            }
        }
    } catch (error) {
        console.error('Error loading announcements:', error);
    }
}

/**
 * Load marks data
 */
async function loadMarksData(studentId) {
    try {
        const result = await API.Marks.getStudentMarks(studentId);
        
        if (result.success && result.data) {
            const marksElement = document.getElementById('recentMarks');
            
            if (marksElement) {
                marksElement.innerHTML = '';
                
                if (result.data.length === 0) {
                    marksElement.innerHTML = '<p>No marks available.</p>';
                    return;
                }
                
                // Display recent marks (last 5)
                result.data.slice(0, 5).forEach(mark => {
                    const markDiv = document.createElement('div');
                    markDiv.className = 'mark-item';
                    markDiv.innerHTML = `
                        <span>${mark.subject || 'Subject'}</span>
                        <span>${mark.marks || 0}/${mark.total || 100}</span>
                    `;
                    marksElement.appendChild(markDiv);
                });
            }
        }
    } catch (error) {
        console.error('Error loading marks:', error);
    }
}

/**
 * Logout function
 */
async function logout() {
    try {
        await API.Auth.logout();
        localStorage.removeItem('studentId');
        window.location.href = '/student-login';
    } catch (error) {
        console.error('Error logging out:', error);
        // Redirect anyway
        window.location.href = '/student-login';
    }
}

// Expose logout function globally if needed
window.studentLogout = logout;
