from django.contrib import admin

# Register your models here.
from projectapp.models import User, Treatment, Reservation, Rating, FAQ

admin.site.register(User)
admin.site.register(Treatment)
admin.site.register(Reservation)
admin.site.register(Rating)
admin.site.register(FAQ)
