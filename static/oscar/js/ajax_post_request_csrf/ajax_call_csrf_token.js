
/*Storing the CSRF token in a cookie (Django’s default) is safe, want to store it in sessions
          CSRF_USE_SESSIONS and CSRF_COOKIE_HTTPONLY are set to True.
              By default, Django stored CSRF token in Cookie. So, CSRF_USE_SESSIONS and CSRF_COOKIE_HTTPONLY are False. */

// Acquiring the token if CSRF_USE_SESSIONS and CSRF_COOKIE_HTTPONLY are False¶
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

/* Setting the token on the AJAX request */

/* Following methods like GET are safe */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// headers to be set on every request i.e. POST request
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});