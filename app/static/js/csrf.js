// Get CSRF token from meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Set up CSRF token for all fetch requests
const originalFetch = window.fetch;
window.fetch = function() {
    let [resource, config] = arguments;
    if (config === undefined) {
        config = {};
    }
    if (config.headers === undefined) {
        config.headers = {};
    }
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(config.method || 'GET')) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return originalFetch(resource, config);
};

// Set up CSRF token for all jQuery AJAX requests (if jQuery is used)
if (typeof $ !== 'undefined') {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });
}
