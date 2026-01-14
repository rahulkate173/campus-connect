import { supabase } from './supabase-config.js';

const loginForm = document.getElementById('parentLoginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI Feedback
    btnText.innerText = "Connecting to Portal...";
    submitBtn.disabled = true;

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Supabase Sign In
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password,
    });

    if (error) {
        alert("Parent Login Error: " + error.message);
        btnText.innerText = "Access Portal";
        submitBtn.disabled = false;
    } else {
        console.log("Parent Logged In Successfully");
        // Redirect to parent-specific view
        window.location.href = 'parent-dashboard.html';
    }
});