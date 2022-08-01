from django.contrib import admin

# Register your models here.
from projectapp.models import User, Treatment, Reservation, Date, Hour

admin.site.register(User)
admin.site.register(Treatment)
admin.site.register(Reservation)
admin.site.register(Date)
admin.site.register(Hour)