/**
 * Student Login Script
 */

const loginForm = document.getElementById('loginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI State: Loading
        btnText.innerText = "Authenticating...";
        submitBtn.disabled = true;

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            // Call the API
            const result = await API.Auth.login(email, password);

            if (result.success) {
                // Success - redirect to student dashboard
                console.log("Student login successful");
                window.location.href = '/student/dashboard';
            } else {
                // Error from API
                alert("Login Failed: " + (result.error || "Unknown error"));
                btnText.innerText = "Sign In";
                submitBtn.disabled = false;
            }
        } catch (error) {
            // Network or other error
            alert("Login Failed: " + error.message);
            btnText.innerText = "Sign In";
            submitBtn.disabled = false;
        }
    });
}
