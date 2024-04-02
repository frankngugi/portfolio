from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Events, Payment, Member, RegisteredEvent

# Register your models here.
admin.site.register(Events)
admin.site.register(Payment)
admin.site.register(Member)
admin.site.register(RegisteredEvent)