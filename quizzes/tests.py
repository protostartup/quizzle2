from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .models import Quiz, Question, Category
from django.utils.html import escape
import json

class QuizDisplayTest(TestCase):
    """ The dashboard upon login displays correctly. """
    fixtures = ['fixtures/test_data.json']

    def setUp(self):
        """ Create request and user """
        self.factory = RequestFactory()
        self.student = User.objects.create_user(username="sample_student", password="sample_pass",
                                                first_name="Sample", last_name="Student")
        self.client = Client()
        self.client.login(username='sample_student', password='sample_pass')

        # Create a new survey
        quiz = Quiz.objects.create(student=self.student,
                               num_questions=4,
                               question_ids=json.dumps(list(range(1,5))),
                               quiz_num_for_student=1)

        self.quiz = quiz

    def test_that_questions_loaded_fixtures(self):
        """ Test that there are at least 10 questions and  categories in the database """
        self.assertEqual(Question.objects.all().count(), 4)
        self.assertEqual(Category.objects.all().count(), 4)


    def test_that_all_questions_are_displayed(self):
        """
        Traverse the entire quiz.
        Pull questions from the database and make sure each question
        from the database is on the quiz.
        """
        for i in range(1,5):
            response = self.client.get('/quiz/{}/question/{}'.format(self.quiz.id, i))
            question_text = escape(Question.objects.get(pk=i).question_text)
            self.assertContains(response, question_text, status_code=200)
