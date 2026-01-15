/**
 * Parent Login Script
 */

const parentLoginForm = document.getElementById('parentLoginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');

if (parentLoginForm) {
    parentLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI State: Loading
        btnText.innerText = "Connecting to Portal...";
        submitBtn.disabled = true;

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            // Call the API
            const result = await API.Auth.login(email, password);

            if (result.success) {
                // Success - redirect to parent dashboard
                console.log("Parent login successful");
                window.location.href = '/parent/dashboard';
            } else {
                // Error from API
                alert("Parent Login Error: " + (result.error || "Unknown error"));
                btnText.innerText = "Access Portal";
                submitBtn.disabled = false;
            }
        } catch (error) {
            // Network or other error
            alert("Parent Login Error: " + error.message);
            btnText.innerText = "Access Portal";
            submitBtn.disabled = false;
        }
    });
}
