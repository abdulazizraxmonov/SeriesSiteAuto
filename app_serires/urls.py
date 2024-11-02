from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('series/<int:pk>/', views.series_detail, name='series_detail'),
    path('episode/<int:pk>/', views.episode_detail, name='episode_detail'),
    path('search/', views.search_series, name='search_series'),  # Добавлен маршрут для поиска
    path('add-comment/<int:episode_pk>/', views.add_comment, name='add_comment'),  # Изменено на дефис
    path('country/<int:country_id>/', views.country_series, name='country_series'),
    path('genre/<int:genre_id>/', views.genre_series, name='genre_series'),
    path('load-more-series/', views.load_more_series, name='load_more_series'),  
    path('sorted/<str:sort_type>/', views.series_sorted, name='series_sorted'),  # Не забудьте реализовать представление
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/login/', views.user_login, name='login'),
    path('fragments/', views.fragment_list, name='fragment_list'),
    path('fragments/<int:fragment_id>/', views.fragment_detail, name='fragment_detail'),
    path('search_series/', views.search_series, name='search_series'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('about/', views.about_view, name='about'),
    
]