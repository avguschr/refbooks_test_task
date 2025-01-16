from django.contrib import admin
from django.contrib.auth.models import Group

from refbooks.models import *

admin.site.register(Refbook)
admin.site.register(RefbookVersion)
admin.site.register(RefbookElement)
admin.site.unregister(Group)
