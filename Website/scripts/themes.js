
(function(){
    // Helper to get cookie value
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }

    // Helper to set cookie
    function setCookie(name, value, days = 7) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
    }

    // Check or set the style
    let style = getCookie('style');
    if (!style) {
        style = 'standard';
        setCookie('style', style);
    }

    // Create and insert the stylesheet link
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `/alt-styles/${style}.css`;
    document.head.appendChild(link);
})();