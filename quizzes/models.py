from django.db import models
from django.utils.text import slugify
import itertools
from django.contrib.auth.models import User


class Category(models.Model):
    """Categories that questions can be in"""
    name = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=False)
    description = models.TextField(default="Description for Category")
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def active_questions(self):
        return self.questions.filter(active=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            max_length = 200
            self.slug = orig = slugify(self.name)[:max_length]

            for x in itertools.count(1):
                if not Question.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        return super(Category, self).save(*args, **kwargs)


class Question(models.Model):

    question_text = models.CharField(max_length=200)
    title = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    # Access all choices through related_name "choices"

    def save(self, *args, **kwargs):
        if not self.slug:
            max_length = 200
            self.slug = orig = slugify(self.question_text)[:max_length]

            for x in itertools.count(1):
                if not Question.objects.filter(slug=self.slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        return super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_correct = models.BooleanField()
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text



class Quiz(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_num_for_student = models.IntegerField()
    question_ids = models.TextField()
    num_questions = models.IntegerField()
    complete = models.BooleanField(default=False)
    final_score = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return "Quiz {}".format(self.quiz_num_for_student)




class QuestionResponse(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="responses", null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice,  on_delete=models.CASCADE)
    attempt_number = models.PositiveSmallIntegerField(blank=True, null=True)

    # Note attempt number is the number of attempts on this quiz or in free form