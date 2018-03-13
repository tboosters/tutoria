# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import UserProfile
from .models import Admin
from .models import Student
from .models import Tutor
from .models import Tag
from .models import TimeSlot
from .models import University
from .models import Review

admin.site.register(UserProfile)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Tag)
admin.site.register(TimeSlot)
admin.site.register(University)
admin.site.register(Review)