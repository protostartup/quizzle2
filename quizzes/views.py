from django.shortcuts import render, redirect, reverse
from .models import Category, Question, Quiz, QuestionResponse, Choice
from django.shortcuts import get_object_or_404
import random
import json

def home_view(request):

    user = request.user

    if not user.is_authenticated:
        return render(request, "homepage.html")

    context = {
        "welcome_message": "Hello, and welcome {}!".format(user),
        "categories": [{"name": cat.name, "id": cat.id} for cat in Category.objects.filter(active=True)],
        "quizzes": Quiz.objects.filter(student=request.user),
    }

    return render(request, "quizzes/dashboard.html", context)



def create_quiz(request):

    if request.method == "POST":

        # This is ineffcient of course
        data = dict(request.POST)
        print(data)
        # print("Categories is {}".format(dict(data).get('categories')))
        questions = Question.objects.filter(category__pk__in=data['categories'])
        num_questions = sample_size = int(data.get("num_questions")[0])
        print(list(questions))

        question_on_quiz = [q.id for q in random.sample(list(questions), sample_size)]

        print("Quiz qs {}".format(question_on_quiz))

        quiz_num_for_student = Quiz.objects.filter(student=request.user).count() + 1

        Quiz.objects.create(student=request.user,
                               num_questions=num_questions,
                               question_ids=json.dumps(question_on_quiz),
                               quiz_num_for_student=quiz_num_for_student)

    return redirect(reverse("home"))

def quiz_question_view(request, quiz_id, question_id):

    quiz = get_object_or_404(Quiz, pk=quiz_id, student=request.user),
    question = get_object_or_404(Question, pk=question_id)

    # try:
    #     question_response = QuestionResponse.get.create(
    #         student=request.user,
    #         question=question,
    #     )

    if request.method == "POST":
        answer_id = request.POST.get("answer-chosen")
        choice = Choice.objects.get(id=answer_id)
        question_response = QuestionResponse.objects.create(
                                student=request.user,
                                question=question,
                                choice=choice
                            )
        context = {"question_response": question_response}
        return render(request, "quizzes/quiz_feedback.html", context)

    context = {
        "quiz": quiz,
        "question": question,
    }

    return render(request, "quizzes/quiz.html", context)

def quiz_view(request, id):

    quiz = get_object_or_404(Quiz, pk=id, student=request.user)
    questions = json.loads(quiz.question_ids)
    first_question_id = questions[0]

    return redirect("quizzes:quiz-question-view", quiz_id=id, question_id=first_question_id)



