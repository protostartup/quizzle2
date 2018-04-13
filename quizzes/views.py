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
        num_questions = int(data.get("num_questions")[0])
        print(list(questions))

        sample_size = num_questions if num_questions < len(questions) else len(questions)
        print(sample_size)

        question_on_quiz = [q.id for q in random.sample(list(questions), sample_size)]

        print("Quiz qs {}".format(question_on_quiz))

        quiz_num_for_student = Quiz.objects.filter(student=request.user).count() + 1

        quiz = Quiz.objects.create(student=request.user,
                               num_questions=num_questions,
                               question_ids=json.dumps(question_on_quiz),
                               quiz_num_for_student=quiz_num_for_student)

    return redirect("quizzes:quiz-view", id=quiz.id)

def quiz_question_view(request, quiz_id, question_id):

    quiz = get_object_or_404(Quiz, pk=quiz_id, student=request.user)
    question = get_object_or_404(Question, pk=question_id)

    question_ids = json.loads(quiz.question_ids)
    questions_dict = dict(zip(range(len(question_ids)), question_ids))
    prev_question_id = questions_dict.get(question_ids.index(question_id) - 1)
    next_question_id = questions_dict.get(question_ids.index(question_id) + 1)

    context = {"quiz": quiz,
               "prev_question_id": prev_question_id,
               "next_question_id": next_question_id,
               }

    print(quiz)

    try:
        question_response = QuestionResponse.objects.get(
            student=request.user,
            question=question,
            quiz=quiz,
        )


        context['question_response'] = question_response

        return render(request, "quizzes/question_feedback.html", context)

    except QuestionResponse.DoesNotExist:
        pass

    if request.method == "POST":
        answer_id = request.POST.get("answer-chosen")
        choice = Choice.objects.get(id=answer_id)
        question_response = QuestionResponse.objects.create(
                                student=request.user,
                                quiz=quiz,
                                question=question,
                                choice=choice
                            )
        context['question_response'] = question_response
        return render(request, "quizzes/question_feedback.html", context)

    # Request is GET and has not been seen before

    context['question'] = question
    return render(request, "quizzes/question_detail.html", context)

def quiz_view(request, id):

    quiz = get_object_or_404(Quiz, pk=id, student=request.user)
    questions = json.loads(quiz.question_ids)
    first_question_id = questions[0]

    return redirect("quizzes:quiz-question-view", quiz_id=id, question_id=first_question_id)


def quiz_results(request, quiz_id):

    quiz = get_object_or_404(Quiz, pk=quiz_id, student=request.user)
    quiz.complete = True
    quiz.save()

    total_score = (len(quiz.responses.all().filter(choice__is_correct=True))/len(quiz.responses.all())) * 100

    context = {"quiz": quiz,
               "total_score": total_score}
    return render(request, "quizzes/quiz_results.html", context)


def categories_view(request):

    categories = Category.objects.filter(active=True)
    context = {"categories": categories}

    return render(request, "quizzes/categories.html", context)


def category_detail_view(request, slug):

    category = get_object_or_404(Category, slug=slug)
    questions = category.active_questions()

    for q in questions:
        has_attempted = QuestionResponse.objects.filter(question=q, quiz=None).exists()
        q.has_attempted = has_attempted


    context = {"category": category, "personal_questions": questions}

    return render(request, "quizzes/category_detail.html", context)


def question_detail_view(request, slug):


    question = get_object_or_404(Question, slug=slug)
    context = {"question": question}

    if request.method == "POST":
        answer_id = request.POST.get("answer-chosen")
        choice = Choice.objects.get(id=answer_id)
        question_response = QuestionResponse.objects.create(
            student=request.user,
            quiz=None,
            question=question,
            choice=choice
        )
        context['question_response'] = question_response
        return render(request, "quizzes/question_feedback.html", context)


    question_response = QuestionResponse.objects.filter(student=request.user, question=question, quiz=None).first()
    if question_response:
        context['question_response'] = question_response
        print("Found question response {}".format(question_response))
        return render(request, "quizzes/question_feedback.html", context)




    return render(request, "quizzes/question_detail.html", context)



