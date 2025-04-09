// Function to delete all cookies available on the current path
function deleteAllCookies() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
        document.cookie = `${name}=; Max-Age=0; path=/`;
    }
    
    // Redirect to login page
    window.location.href = 'login';
}


