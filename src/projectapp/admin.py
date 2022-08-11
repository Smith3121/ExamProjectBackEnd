from django.contrib import admin

# Register your models here.
from projectapp.models import User, Treatment, Reservation

admin.site.register(User)
admin.site.register(Treatment)
admin.site.register(Reservation)
