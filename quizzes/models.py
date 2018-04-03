from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    """Categories that questions can be in"""
    name = models.CharField(max_length=200, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Question(models.Model):

    question_text = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
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


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_correct = models.BooleanField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text



class Quiz(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_num_for_student = models.IntegerField()
    question_ids = models.TextField()
    num_questions = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QuestionResponse(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()