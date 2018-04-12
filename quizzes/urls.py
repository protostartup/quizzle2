from django.urls import include, path
from . import views

app_name = "quizzes"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("create-quiz", views.create_quiz, name="create-quiz"),
    path("quiz/<int:id>", views.quiz_view, name="quiz-view"),
    path("quiz/<int:quiz_id>/question/<int:question_id>", views.quiz_question_view, name="quiz-question-view"),
    path("quiz/<int:quiz_id>/results", views.quiz_results, name="quiz-results-view"),
    path("quiz", views.categories_view, name="categories"),
]