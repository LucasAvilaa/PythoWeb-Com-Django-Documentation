from django.contrib import admin
from django.contrib.admin.helpers import AdminField

from .models import Question

admin.site.register(Question)
