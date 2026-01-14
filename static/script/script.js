import { supabase } from './supabase-config.js';

const loginForm = document.getElementById('loginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI State: Loading
    btnText.innerText = "Authenticating...";
    submitBtn.disabled = true;

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Supabase Sign In
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password,
    });

    if (error) {
        // UI State: Error
        alert("Login Failed: " + error.message);
        btnText.innerText = "Sign In";
        submitBtn.disabled = false;
    } else {
        // UI State: Success
        console.log("Login successful:", data);
        window.location.href = 'dashboard.html';
    }
});