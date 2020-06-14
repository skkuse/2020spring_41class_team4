from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Post)
admin.site.register(Schedule)
admin.site.register(Course)
admin.site.register(Locker)

