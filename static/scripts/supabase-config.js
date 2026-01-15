/**
 * API Configuration and Helper Functions for Campus Connect
 * This file provides a unified interface to interact with the backend API
 */

// API base URL - change this for production
const API_BASE_URL = window.location.origin;

/**
 * Generic fetch wrapper with error handling
 */
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies for session management
    };

    const config = { ...defaultOptions, ...options };
    
    // Merge headers
    if (options.headers) {
        config.headers = { ...defaultOptions.headers, ...options.headers };
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * Authentication API methods
 */
const AuthAPI = {
    login: async (email, password) => {
        return apiRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },

    logout: async () => {
        return apiRequest('/api/auth/logout', {
            method: 'POST'
        });
    }
};

/**
 * Profile API methods
 */
const ProfileAPI = {
    getProfile: async (userId) => {
        return apiRequest(`/api/profile/${userId}`);
    },

    updateProfile: async (userId, data) => {
        return apiRequest(`/api/profile/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
};

/**
 * Classroom API methods
 */
const ClassroomAPI = {
    getAllClassrooms: async () => {
        return apiRequest('/api/classrooms');
    },

    getClassroom: async (classYear) => {
        return apiRequest(`/api/classroom/${classYear}`);
    },

    getTimetable: async (classYear) => {
        return apiRequest(`/api/classroom/${classYear}/timetable`);
    },

    updateTimetable: async (classYear, timetable) => {
        return apiRequest(`/api/classroom/${classYear}/timetable`, {
            method: 'PUT',
            body: JSON.stringify({ timetable })
        });
    }
};

/**
 * Attendance API methods
 */
const AttendanceAPI = {
    getStudentAttendance: async (studentId) => {
        return apiRequest(`/api/attendance/${studentId}`);
    },

    createAttendance: async (data) => {
        return apiRequest('/api/attendance', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    updateAttendance: async (attendanceId, data) => {
        return apiRequest(`/api/attendance/${attendanceId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
};

/**
 * Assignment API methods
 */
const AssignmentAPI = {
    getAssignments: async (classroomId) => {
        return apiRequest(`/api/assignments/${classroomId}`);
    },

    createAssignment: async (data) => {
        return apiRequest('/api/assignments', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    updateAssignment: async (assignmentId, data) => {
        return apiRequest(`/api/assignments/${assignmentId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    deleteAssignment: async (assignmentId) => {
        return apiRequest(`/api/assignments/${assignmentId}`, {
            method: 'DELETE'
        });
    }
};

/**
 * Marks API methods
 */
const MarksAPI = {
    getStudentMarks: async (studentId) => {
        return apiRequest(`/api/marks/${studentId}`);
    },

    createMarks: async (data) => {
        return apiRequest('/api/marks', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    updateMarks: async (markId, data) => {
        return apiRequest(`/api/marks/${markId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
};

/**
 * Announcement API methods
 */
const AnnouncementAPI = {
    getAnnouncements: async (role = null) => {
        const endpoint = role ? `/api/announcements?role=${role}` : '/api/announcements';
        return apiRequest(endpoint);
    },

    createAnnouncement: async (data) => {
        return apiRequest('/api/announcements', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    deleteAnnouncement: async (announcementId) => {
        return apiRequest(`/api/announcements/${announcementId}`, {
            method: 'DELETE'
        });
    }
};

/**
 * Student API methods
 */
const StudentAPI = {
    getStudentsByClass: async (classYear) => {
        return apiRequest(`/api/students/${classYear}`);
    }
};

/**
 * Parent API methods
 */
const ParentAPI = {
    getChildInfo: async (parentId) => {
        return apiRequest(`/api/parent/${parentId}/child`);
    }
};

// Export all API modules
const API = {
    Auth: AuthAPI,
    Profile: ProfileAPI,
    Classroom: ClassroomAPI,
    Attendance: AttendanceAPI,
    Assignment: AssignmentAPI,
    Marks: MarksAPI,
    Announcement: AnnouncementAPI,
    Student: StudentAPI,
    Parent: ParentAPI
};

// For module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
