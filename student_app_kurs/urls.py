"""
URL configuration for student_app_kurs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views  # Импортируем представления из views.py
from django.conf import settings
from django.conf.urls.static import static
from .views import statistics_view  # убедись, что импортируется
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.register, name='home'),  # Главная страница
    path('admin/', admin.site.urls),   # Маршрут для админки
    path('register/', views.register, name='register'),  # Страница регистрации
    path('login/', views.user_login, name='login'),      # Страница входа
    path('tests/', views.test_list, name='test_list'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('profile/', views.profile, name='profile'),
   # path('tests/schulte/', views.schulte_test, name='schulte_test'),
   # path('tests/schulte/submit/', views.schulte_submit, name='schulte_submit'),
    path('statistics/', statistics_view, name='statistics'),
# Рекомендации (общий список)
    path('recommendations/', views.recommendations_list, name='recommendations'),
    # Выполнение рекомендации (чтобы пометить её как выполненную)
    path(
        'recommendations/submit/<int:result_id>/<int:rec_id>/',
        views.submit_recommendation,
        name='submit_recommendation'
    ),
    #Тест Шульте
    path('schulte/', views.schulte_test, name='schulte_test'),
    path('strup/', views.strup_test, name='strup_test'),
    path('save_schulte_result/', views.save_schulte_result, name='save_schulte_result'),
    path('strup/save/', views.save_strup_result, name='save_strup_result'),
    path('nback/', views.nback_test, name='nback_test'),
    path('nback/save/', views.save_nback_result, name='save_nback_result'),
    path('cpt/', views.cpt_test, name='cpt_test'),
    path('save_cpt_result/', views.save_cpt_result, name='save_cpt_result'),
    path('spilberger/', views.spilberger_test, name='spilberger_test'),
    path('save_spilberger_result/', views.save_spilberger_result, name='save_spilberger_result'),
    path('bdi/', views.bdi_test, name='bdi_test'),
    path('save_bdi_result/', views.save_bdi_result, name='save_bdi_result'),

# пути к рекомендациям
    path('recommendations/schulte/', views.schulte_recommendation, name='schulte_recommendation'),
    path('recommendations/strup/', views.strup_recommendation, name='strup_recommendation'),
    path('recommendations/nback/', views.nback_recommendation, name='nback_recommendation'),
    path('recommendations/cpt/', views.cpt_recommendation, name='cpt_recommendation'),
    path('recommendations/spilberger/', views.spilberger_recommendation, name='spilberger_recommendation'),
    path('recommendations/bdi/', views.bdi_recommendation, name='bdi_recommendation'),

path('schulte/result/', views.schulte_result_view, name='schulte_result'),

    # пути к упражнениям
    path('practice/schulte/', views.schulte_practice, name='schulte_practice'),
    path('practice/strup/', views.strup_practice, name='strup_practice'),
    path('practice/nback/', views.nback_practice, name='nback_practice'),
    path('practice/cpt/', views.cpt_practice, name='cpt_practice'),
    path('practice/spilberger/', views.spilberger_practice, name='spilberger_practice'),
    path('practice/bdi/', views.bdi_practice, name='bdi_practice'),


path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

path('upload_photo/', views.upload_photo, name='upload_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

