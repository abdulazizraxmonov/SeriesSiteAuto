from django.contrib import admin
from .models import Genre, Series, Episode, Comment, Country, Fragment, ReleaseSchedule, About, CopyrightHolder

admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Series)
admin.site.register(Episode)
admin.site.register(Comment)
admin.site.register(Fragment)
admin.site.register(ReleaseSchedule)
admin.site.register(About)
admin.site.register(CopyrightHolder)
