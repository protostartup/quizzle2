from django.urls import include, path
from . import views

app_name = "quizzes"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("create-quiz/", views.create_quiz, name="create-quiz"),
    path("quiz/<int:id>", views.quiz_view, name="quiz-view"),
    path("quiz/<int:quiz_id>/question/<int:question_id>", views.quiz_question_view, name="quiz-question-view"),
    path("quiz/<int:quiz_id>/results", views.quiz_results, name="quiz-results-view"),
    path("categories/", views.categories_view, name="categories"),
    path("categories/<slug:slug>/", views.category_detail_view, name="category-detail-view"),
    path("question/<slug:slug>/", views.question_detail_view, name="question-detail-view"),
    path("question/try-again/<int:question_id>", views.try_again_view, name="try-again-view"),
]