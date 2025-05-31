from django.db import models
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username

class Test(models.Model):
    # Уникальный ID теста (в Django это будет автоматически через первичный ключ)
    title = models.CharField(max_length=255)  # Название теста
    description = models.TextField()  # Описание теста
    is_mandatory = models.BooleanField(default=False)  # <- Новое поле
    def __str__(self):
        return self.title  # Строковое представление для удобства

class Question(models.Model):
    # Связь с тестом
    test = models.ForeignKey('Test', on_delete=models.CASCADE)  # Внешний ключ, ссылающийся на модель Test
    question_text = models.TextField()  # Текст вопроса
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('single_choice', 'Single Choice'),
            ('multi_choice', 'Multi Choice'),
            ('open', 'Open')
        ]
    )  # Тип вопроса (с использованием ENUM как ограничение значений)
    correct_answer = models.TextField(null=True, blank=True)  # Правильный ответ (если применимо)

    def __str__(self):
        return self.question_text[:50]  # Возвращаем первые 50 символов вопроса для удобства

class Result(models.Model):
    # Связь с пользователем
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Внешний ключ, ссылающийся на модель User
    # Связь с тестом
    test = models.ForeignKey('Test', on_delete=models.CASCADE)  # Внешний ключ, ссылающийся на модель Test
    test_date = models.DateTimeField()  # Дата прохождения теста
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Результат в баллах
    hours_worked = models.IntegerField(default=0)  # Количество отработанных часов
    work_intensity = models.CharField(
        max_length=10,
        choices=[
            ('none', 'None'),
            ('physical', 'Physical'),
            ('moderate', 'Moderate'),
            ('mental', 'Mental')
        ],
        default='none'  # Интенсивность работы
    )
    follow_up_checked = models.BooleanField(default=False)  # Проверялось ли выполнение рекомендаций

    def __str__(self):
        return f"Result for {self.user.name} in {self.test.title} on {self.test_date}"

class Recommendation(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    text = models.TextField()
    level_min = models.IntegerField()
    level_max = models.IntegerField()

    def __str__(self):
        return f"Рекомендация для {self.test.title}"

class Practice(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    level_min = models.IntegerField()
    level_max = models.IntegerField()

from django.db import models
from django.conf import settings

class RecommendationTracking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
    recommendation = models.ForeignKey('Recommendation', on_delete=models.CASCADE)
    completion_status = models.CharField(
        max_length=20,
        choices=[
            ('completed', 'Completed'),
            ('partial', 'Partial'),
            ('not_completed', 'Not Completed')
        ]
    )
    feedback = models.TextField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Tracking: {self.user} – {self.recommendation.test.title} [{self.completion_status}]"

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_freshman = models.BooleanField(default=False)
    is_nonresident = models.BooleanField(default=False)
    is_international = models.BooleanField(default=False)
    is_employed = models.BooleanField(default=False)
    WORK_INTENSITY_CHOICES = [
        ('none', 'Не работаю'),
        ('physical', 'Тяжелый физический труд'),
        ('moderate', 'Умеренная нагрузка'),
    ]
    work_intensity = models.CharField(max_length=20, choices=WORK_INTENSITY_CHOICES, default='none')

    def __str__(self):
        return f"{self.user.username} Profile"

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    score = models.FloatField()
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title}: {self.score}"

#ест Таблицы Шульте
class SchulteResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    average_time = models.FloatField()  # Время выполнения одного поля
    total_time = models.FloatField()    # Общее время прохождения теста

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

# Тест Струпа
from django.db import models
from django.conf import settings

class StroopResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_taken = models.FloatField()
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

#nBack тест

class NBackResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NBackResult for {self.user} at {self.timestamp}"


# CPT тест


class CPTResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    correct_hits = models.IntegerField(default=0)
    false_alarms = models.IntegerField(default=0)
    misses = models.IntegerField(default=0)
    time_taken = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CPTResult for {self.user} at {self.timestamp}"

# Шкала Спилбергера_Ханина

class SpilbergerResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SpilbergerResult for {self.user} at {self.timestamp}"


#BDI тест

class BDIResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BDIResult for {self.user} at {self.timestamp}"
