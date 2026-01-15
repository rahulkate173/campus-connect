/**
 * Faculty Login Script
 */

const facultyLoginForm = document.getElementById('facultyLoginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');

if (facultyLoginForm) {
    facultyLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI State: Loading
        btnText.innerText = "Launching Dashboard...";
        submitBtn.disabled = true;

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            // Call the API
            const result = await API.Auth.login(email, password);

            if (result.success) {
                // Success - redirect to faculty dashboard
                console.log("Faculty login successful");
                window.location.href = '/faculty/dashboard';
            } else {
                // Error from API
                alert("Login Failed: " + (result.error || "Unknown error"));
                btnText.innerText = "Launch Dashboard";
                submitBtn.disabled = false;
            }
        } catch (error) {
            // Network or other error
            alert("Login Failed: " + error.message);
            btnText.innerText = "Launch Dashboard";
            submitBtn.disabled = false;
        }
    });
}
