from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Series(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='series')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    popularity = models.PositiveIntegerField(default=0)
    poster_url = models.URLField(blank=True)
    rating = models.FloatField(default=0) 
    release_year = models.PositiveIntegerField(null=True, blank=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    

from django.db import models

class Episode(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    mover_url = models.URLField(help_text="URL эпизода на mover.uz", null=True, blank=True)
    video_file = models.FileField(upload_to='episodes/', null=True, blank=True)
    add_method = models.CharField(max_length=10, choices=[('url', 'URL'), ('file', 'File')], default='url')  # Добавьте это поле, если его нет

    def __str__(self):
        return f"{self.series.title} - Эпизод {self.episode_number}"

class Fragment(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='fragments')
    title = models.CharField(max_length=255)
    video_url = models.URLField(help_text="Ссылка на видео фрагмента", null=True, blank=True)

    def __str__(self):
        return self.title
    
class ReleaseSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]

    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='release_schedules')
    release_day = models.CharField(max_length=3, choices=DAYS_OF_WEEK, default='mon')
    release_time = models.TimeField()  # Время выхода серии

    def __str__(self):
        return f"{self.series.title} - {self.get_release_day_display()} в {self.release_time.strftime('%H:%M')}"

class Comment(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Комментарий от {self.author.username}"


class About(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CopyrightHolder(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()  # Это может быть email, телефон и т. д.
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

