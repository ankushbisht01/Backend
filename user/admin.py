from django.contrib import admin
from user.models import User , Tour , Rating
# Register your models here.

admin.site.register([
    User,
    Tour,
    Rating , 
])
