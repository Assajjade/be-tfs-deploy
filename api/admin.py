from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Trip)
admin.site.register(UserTrip)
admin.site.register(History)
admin.site.register(VolunteerMetrics)
admin.site.register(Merchandise)
admin.site.register(Fund)
admin.site.register(Blog)
admin.site.register(UserMetrics)
admin.site.register(TripQuestion)
admin.site.register(TripAnswer)
admin.site.register(MerchandiseSection)
admin.site.register(AboutUs)

