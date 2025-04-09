// Check for the airsloggedin cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// If airsloggedin is not set or not true, redirect to login
const isLoggedIn = getCookie('airsloggedin');
if (!isLoggedIn || isLoggedIn !== 'true') {
    window.location.href = 'login';
}
