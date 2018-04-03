from django.shortcuts import render

def home_view(request):

    user = request.user

    if not user.is_authenticated:
        return render(request, "homepage.html")

    context = {
        "welcome_message": "Hello, and welcome {}!".format(user)
    }

    return render(request, "quizzes/dashboard.html", context)

