import { supabase } from './supabase-config.js';

const signupForm = document.getElementById('signupForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI Feedback
    btnText.innerText = "Creating Account...";
    submitBtn.disabled = true;

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const captchaChecked = document.querySelector('input[name="captcha"]').checked;

    // Simple CAPTCHA validation
    if (!captchaChecked) {
        alert("Please confirm you are not a robot.");
        btnText.innerText = "Create Account";
        submitBtn.disabled = false;
        return;
    }

    // Supabase Sign Up
    const { data, error } = await supabase.auth.signUp({
        email: email,
        password: password,
        options: {
            data: {
                full_name: name,
                role: "student"
            }
        }
    });

    if (error) {
        alert("Student Signup Error: " + error.message);
        btnText.innerText = "Create Account";
        submitBtn.disabled = false;
    } else {
        console.log("Student Registered Successfully");

        alert(
            "Account created successfully. Please check your university email to verify your account."
        );

        // Redirect after successful signup
        window.location.href = 'studentlogin.html';
    }
});
