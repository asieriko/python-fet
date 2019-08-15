from django.contrib import admin
from cServer.models import Computer, Thread, File, Assignment, Result

admin.site.register(Computer)
admin.site.register(Thread)
admin.site.register(File)
admin.site.register(Assignment)
admin.site.register(Result)
