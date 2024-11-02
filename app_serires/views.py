from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Series, Episode, Comment, Genre, Country

from django.shortcuts import render
from .models import Series, Genre, Country

def home(request):
    genres = Genre.objects.all()
    countries = Country.objects.all()

    # Получаем параметры сортировки и фильтрации из запроса
    sort_type = request.GET.get('sort_type', '')
    country_id = request.GET.get('country', '')
    genre_id = request.GET.get('genre', '')

    # Начальная выборка
    series_queryset = Series.objects.all()

    # Применение фильтров
    if country_id:
        series_queryset = series_queryset.filter(country__id=country_id)

    if genre_id:
        series_queryset = series_queryset.filter(genres__id=genre_id)

    # Применение сортировки
    if sort_type == 'year':
        series_queryset = series_queryset.order_by('-release_year')
    elif sort_type == 'popularity':
        series_queryset = series_queryset.order_by('-clicks')  # Изменено на 'clicks'
    elif sort_type == 'new':
        series_queryset = series_queryset.order_by('-id')

    # Получаем все серии
    latest_series = series_queryset.distinct()  # Убедитесь, что результаты уникальны, если применены фильтры

    return render(request, 'home.html', {
        'latest_series': latest_series,
        'genres': genres,
        'countries': countries,
    })



def series_sorted(request, sort_type):
    genres = Genre.objects.all()
    countries = Country.objects.all()

    # Получаем сериалы и применяем сортировку
    if sort_type == 'year':
        series_queryset = Series.objects.order_by('-release_year')
    elif sort_type == 'popularity':
        series_queryset = Series.objects.order_by('-popularity')
    elif sort_type == 'new':
        series_queryset = Series.objects.order_by('-id')
    else:
        series_queryset = Series.objects.all()  # Если сортировка не задана, возвращаем все

    return render(request, 'home.html', {
        'latest_series': series_queryset,
        'genres': genres,
        'countries': countries,
    })

from django.shortcuts import render, get_object_or_404
from .models import Series, Episode


def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    
    # Увеличиваем количество кликов
    series.clicks += 1
    series.save()  # Сохраняем изменения

    episodes = series.episode_set.all()  # Получаем все эпизоды для данного сериала
    first_episode = episodes.first()  # Первый эпизод, если он существует
    all_series = Series.objects.exclude(pk=pk)

    comments = first_episode.comments.all() if first_episode else []

    return render(request, 'series_detail.html', {
        'series': series,
        'episodes': episodes,
        'first_episode': first_episode,
        'comments': comments,
        'all_series': all_series,
    })


# Детали эпизода
def episode_detail(request, pk):
    episode = get_object_or_404(Episode, pk=pk)
    comments = episode.comments.filter(parent__isnull=True)
    series = episode.series
    return render(request, 'episode_detail.html', {
        'episode': episode,
        'comments': comments,
        'series': series,
    })

# Добавление комментария
@login_required
def add_comment(request, episode_pk):
    episode = get_object_or_404(Episode, pk=episode_pk)
    text = request.POST.get('text')
    parent_id = request.POST.get('parent_id')
    parent = Comment.objects.get(id=parent_id) if parent_id else None
    Comment.objects.create(episode=episode, author=request.user, text=text, parent=parent)
    return redirect('episode_detail', pk=episode_pk)


# Фильтрация сериалов по стране
def country_series(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    series = Series.objects.filter(country=country)
    return render(request, 'country_series.html', {'country': country, 'series': series})

# Фильтрация сериалов по жанру
def genre_series(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    series = Series.objects.filter(genres=genre)  # Many-to-many field for genres
    return render(request, 'genre_series.html', {'genre': genre, 'series': series})

from django.http import JsonResponse
from .models import Series

def load_more_series(request):
    year = request.GET.get('year')
    country_id = request.GET.get('country')
    genre_id = request.GET.get('genre')
    popularity = request.GET.get('popularity')

    series_queryset = Series.objects.all()

    # Применение фильтров
    if year:
        series_queryset = series_queryset.order_by('release_year' if year == 'asc' else '-release_year')

    if country_id:
        series_queryset = series_queryset.filter(country__id=country_id)

    if genre_id:
        series_queryset = series_queryset.filter(genres__id=genre_id)

    if popularity:
        # Изменяем сортировку по количеству кликов
        if popularity == "popular":
            series_queryset = series_queryset.order_by('-clicks')  # Сортируем по кликам
        elif popularity == "newest":
            series_queryset = series_queryset.order_by('-release_year')  # Можно добавить сортировку по новинкам

    # Генерируем HTML для сериалов
    series_html = "".join(f"""
        <div class="series-card">
            <a href="/series/{s.id}">
                <img src="{s.poster_url}" alt="{s.title}">
                <div class="series-info">
                    <h3>{s.title}</h3>
                    <p>Рейтинг: {s.rating}</p>
                    <p>Год выпуска: {s.release_year}</p>
                </div>
            </a>
        </div>
    """ for s in series_queryset)

    return JsonResponse({'series_html': series_html})



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('home')  # Замените 'home' на нужное представление
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}.")
                return redirect('home')
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('home')


from django.shortcuts import render, get_object_or_404
from .models import Fragment

def fragment_list(request):
    fragments = Fragment.objects.all()
    return render(request, 'fragments/fragment_list.html', {'fragments': fragments})

def fragment_detail(request, fragment_id):
    fragment = get_object_or_404(Fragment, pk=fragment_id)
    return render(request, 'fragments/fragment_detail.html', {'fragment': fragment})


from django.http import JsonResponse
from .models import Series

def search_series(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        series = Series.objects.filter(title__icontains=query)[:10]
        results = [
            {
                'id': s.id,
                'title': s.title,
                'poster_url': s.poster_url,  # Поле с URL постера
            }
            for s in series
        ]
    return JsonResponse({'results': results})


from django.shortcuts import render
from .models import ReleaseSchedule

def schedule_view(request):
    schedules = ReleaseSchedule.objects.select_related('series').all()
    return render(request, 'schedule.html', {'schedules': schedules})

from django.shortcuts import render
from .models import About, CopyrightHolder

def about_view(request):
    about_info = About.objects.first()  # Получаем первую запись о нас
    copyright_holders = CopyrightHolder.objects.all()  # Получаем всех правобладателей
    return render(request, 'about.html', {
        'about_info': about_info,
        'copyright_holders': copyright_holders,
    })

