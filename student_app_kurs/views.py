from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import SchulteResult
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Recommendation, RecommendationTracking, Result
from .models import Recommendation, TestResult


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('questionnaire')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import LoginForm  # импортируешь свою форму


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            profile = user.profile

            if not profile.is_freshman and not profile.is_nonresident and not profile.is_international:
                return redirect('questionnaire')
            else:
                return redirect('test_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required(login_url='login')
def test_list(request):
    mandatory = Test.objects.filter(is_mandatory=True)
    suggested = Test.objects.filter(is_mandatory=False)
    completed_count = Result.objects.filter(user=request.user, test__in=mandatory).count()

    context = {
        'mandatory': mandatory,
        'suggested': suggested,
        'completed_count': completed_count,
        'total_mandatory': mandatory.count(),
    }
    return render(request, 'test_list.html', context)


def submit_test(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(Test, id=test_id)
        user = request.user  # Текущий пользователь
        answers = request.POST  # Ответы из формы

        # Подсчет баллов (для single_choice вопросов)
        score = 0
        for question in test.question_set.all():
            user_answer = answers.get(str(question.id), '')
            if user_answer == question.correct_answer:
                score += 1

        # Сохранение результата
        result = Result.objects.create(
            user=user,
            test=test,
            test_date=now(),
            score=score,
        )
        return render(request, 'test_result.html', {'result': result})

    return render(request, 'error.html', {'message': 'Некорректный запрос'})


# Подгрузка рекомендаций
from django.shortcuts import render, get_object_or_404
from .models import Test, Result, Recommendation


def recommendations_list(request):
    user = request.user
    # Все трековые записи, где пользователь пометил рекомендацию выполненной
    rec_tracks = RecommendationTracking.objects.filter(
        user=user,
        completion_status='completed'
    ).order_by('-completion_date')

    # Всего рекомендаций, которые могли быть назначены:
    total_recs = Recommendation.objects.filter(
        test__in=[t.result.test for t in Result.objects.filter(user=user)]
    ).count()

    context = {
        'recs': rec_tracks,
        'completed': rec_tracks.count(),
        'total': total_recs,
    }
    return render(request, 'recommendations.html', context)


def submit_recommendation(request, result_id, rec_id):
    if request.method == 'POST':
        rec = get_object_or_404(Recommendation, id=rec_id)
        result = get_object_or_404(Result, id=result_id)
        RecommendationTracking.objects.create(
            user=request.user,
            result=result,
            recommendation=rec,
            completion_status='completed',
            completion_date=timezone.now()
        )
    return redirect('recommendations')


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


from django.shortcuts import render


def home(request):
    return render(request, 'home.html')  # Убедись, что шаблон home.html существует


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, QuestionnaireForm


def questionnaire(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = request.user.profile
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('test_list')
    else:
        form = QuestionnaireForm(instance=profile)

    return render(request, 'questionnaire.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

# ТЕСТ ТАБЛИЦЫ ШУЛЬТЕ

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TestResult


@login_required
def schulte_test(request):
    return render(request, 'schulte_test.html')


@login_required
def strup_test(request):
    return render(request, 'strup_test.html')


from django.http import JsonResponse
import json

from .models import SchulteResult, TestResult, Test
from django.utils import timezone


@login_required
def save_schulte_result(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user

            if None in (data.get("average_time"), data.get("total_time")):
                return JsonResponse({"error": "missing required fields"}, status=400)

            SchulteResult.objects.create(
                user=user,
                average_time=data["average_time"],
                total_time=data["total_time"],
                test_date=timezone.now()
            )

            test, _ = Test.objects.get_or_create(title="Таблицы Шульте")
            TestResult.objects.create(
                user=user,
                test=test,
                score=data["average_time"],
                test_date=timezone.now()
            )

            return JsonResponse({"status": "ok"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid json"}, status=400)
        except Exception:
            return JsonResponse({"error": "server error"}, status=500)

    return JsonResponse({"error": "method not allowed"}, status=405)

# Тест Струпа

from django.shortcuts import render
from django.http import JsonResponse
from .models import StroopResult
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def strup_test_view(request):
    return render(request, 'strup_test.html')


@csrf_exempt
@login_required
def save_strup_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            time_taken = data.get('time_taken')
            correct = data.get('correct')
            total = data.get('total')
            if None in (time_taken, correct, total):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            StroopResult.objects.create(
                user=request.user,
                time_taken=time_taken,
                correct_answers=correct,
                total_questions=total,
                test_date=timezone.now()
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Results saved successfully'
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to save results'}, status=500)


from .models import NBackResult, CPTResult, SpilbergerResult, BDIResult

# Тест n-back

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def nback_test(request):
    return render(request, 'nback_test.html')


@csrf_exempt
def save_nback_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        correct_answers = data['correct_answers']
        total_rounds = data['total_rounds']
        level = data['level']

        NBackResult.objects.create(
            user=request.user,
            correct_answers=correct_answers,
            total_rounds=total_rounds,
            level=level,
            accuracy=round(correct_answers / total_rounds, 2) if total_rounds > 0 else 0,
            date=timezone.now()
        )

        return JsonResponse({'status': 'ok', 'accuracy': correct_answers / total_rounds if total_rounds > 0 else 0})

    return JsonResponse({'error': 'POST only'}, status=405)

# CPT тест
def cpt_test(request):
    return render(request, 'cpt_test.html')


@csrf_exempt
def save_cpt_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        CPTResult.objects.create(
            user=request.user,
            correct_hits=data['correct_hits'],
            false_alarms=data['false_alarms'],
            misses=data['misses'],
            reaction_time=data['reaction_time'],
            test_duration=data['test_duration'],
            date=timezone.now()
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'POST required'}, status=405)

# Шкала спилбергера-ханина

def spilberger_test(request):
    # Заглушка
    return render(request, 'spilberger_test.html')


@csrf_exempt
def save_spilberger_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        SpilbergerResult.objects.create(
            user=request.user,
            anxiety_score=data['anxiety_score'],
            depression_score=data['depression_score'],
            test_date=timezone.now()
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'POST required'}, status=405)

# BDI тест
def bdi_test(request):
    # Заглушка для BDI теста
    return render(request, 'bdi_test.html')


@csrf_exempt
def save_bdi_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        BDIResult.objects.create(
            user=request.user,
            total_score=data['total_score'],
            test_date=timezone.now()
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def user_recommendations(request):
    user = request.user
    recommendations = []

    # Получаем все результаты пользователя
    results = TestResult.objects.filter(user=user)

    for result in results:
        # Получаем рекомендацию по этому тесту
        try:
            rec = Recommendation.objects.get(test=result.test)
            recommendations.append({
                "test_title": result.test.title,
                "score": result.score,
                "text": rec.text
            })
        except Recommendation.DoesNotExist:
            continue

    return render(request, "recommendations.html", {"recommendations": recommendations})


# СКОЛЬКО ТЕСТОВ ПРОЙДЕНО
from .models import NBackResult, CPTResult, SpilbergerResult, BDIResult, SchulteResult  # и т.д.


def test_count(request):
    user = request.user
    completed = 0
    total_tests = 6

    if NBackResult.objects.filter(user=user).exists():
        completed += 1
    if CPTResult.objects.filter(user=user).exists():
        completed += 1
    if SpilbergerResult.objects.filter(user=user).exists():
        completed += 1
    if BDIResult.objects.filter(user=user).exists():
        completed += 1
    if SchulteResult.objects.filter(user=user).exists():
        completed += 1
    if StroopResult.objects.filter(user=user).exists():
        completed += 1

    # Добавь сюда другие тесты по аналогии

    return render(request, 'test_list.html', {'completed': completed, 'total': total_tests})


# Рекомендации и упражнения

from django.shortcuts import render


# Рекомендации
def schulte_recommendation(request): return render(request, 'recommendations/schulte_recommendation.html')


def strup_recommendation(request): return render(request, 'recommendations/strup_recommendation.html')


def nback_recommendation(request): return render(request, 'recommendations/nback_recommendation.html')


def cpt_recommendation(request): return render(request, 'recommendations/cpt_recommendation.html')


def spilberger_recommendation(request): return render(request, 'recommendations/spilberger_recommendation.html')


def bdi_recommendation(request): return render(request, 'recommendations/bdi_recommendation.html')


# Упражнения
def schulte_practice(request): return render(request, 'practice/schulte_practice.html')


def strup_practice(request): return render(request, 'practice/strup_practice.html')


def nback_practice(request): return render(request, 'practice/nback_practice.html')


def cpt_practice(request): return render(request, 'practice/cpt_practice.html')


def spilberger_practice(request): return render(request, 'practice/spilberger_practice.html')


def bdi_practice(request): return render(request, 'practice/bdi_practice.html')


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        user = request.user
        user.profile.photo = request.FILES['photo']
        user.profile.save()
    return redirect('profile')


from django.shortcuts import render
from .models import SchulteResult
from django.contrib.auth.decorators import login_required


@login_required
def schulte_result_view(request):
    # Получаем последний результат пользователя по тесту Шульте
    try:
        last_result = SchulteResult.objects.filter(user=request.user).latest('timestamp')
    except SchulteResult.DoesNotExist:
        last_result = None

    if last_result:
        # Пример оценки результата — здесь можешь делать логику на основе average_time
        avg_time = last_result.average_time
        if avg_time < 2:
            recommendation = "Отличный результат! Вы обладаете высокой скоростью восприятия."
            description = "Время выполнения одного поля: {:.2f} сек".format(avg_time)
        elif avg_time < 4:
            recommendation = "Хороший результат, но есть куда стремиться."
            description = "Время выполнения одного поля: {:.2f} сек".format(avg_time)
        else:
            recommendation = "Рекомендуется тренировать концентрацию и скорость реакции."
            description = "Время выполнения одного поля: {:.2f} сек".format(avg_time)
    else:
        recommendation = "Результатов пока нет."
        description = ""

    context = {
        "result_value": last_result.total_time if last_result else "—",
        "result_description": description,
        "recommendation_text": recommendation,
    }
    return render(request, "schulte_result.html", context)


def statistics_view(request):
    return render(request, 'statistics.html')  # пока можно просто пустой шаблон

