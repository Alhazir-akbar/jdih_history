from django.contrib import admin
from .models import Peraturan, PeraturanVersion  # Kita akan membuat model ini nanti

admin.site.register(Peraturan)
admin.site.register(PeraturanVersion)
