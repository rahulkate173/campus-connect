// --- Modal Controls ---

function openStudentLogin() {
    document.getElementById("studentModal").style.display = "block";
}

function openTeacherLogin() {
    document.getElementById("teacherModal").style.display = "block";
}
function openParentLogin() {
    document.getElementById("parentModal").style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Close modals if user clicks background
window.onclick = function(event) {
    if (event.target.className === "modal") {
        event.target.style.display = "none";
    }
}

// --- Form Submissions ---

document.getElementById("studentForm").onsubmit = function(e) {
    e.preventDefault();
    alert("Student login successful! Redirecting...");
};

document.getElementById("teacherForm").onsubmit = function(e) {
    e.preventDefault();
    alert("Teacher login successful! Opening Faculty Portal...");
};