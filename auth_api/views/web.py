from django.shortcuts import render


def login_page(request):
    """Render the login HTML page for the root URL ('/').

    GET -> render the `templates/login.html` template.
    POST -> fall back to same page (API login handled elsewhere).
    """
    # If you want POST to be handled here, implement authentication logic or
    # forward to the API endpoint. For now we render the template and let the
    # existing API handle JSON POSTs at /api/auth/login.
    return render(request, "login.html")
