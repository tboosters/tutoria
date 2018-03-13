# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Booking
from .models import Coupon
from .models import Transaction

admin.site.register(Booking)
admin.site.register(Coupon)
admin.site.register(Transaction)
