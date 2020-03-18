# from django standard library
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pivots/', include('pivots.urls')),
    path('pivots/api/', include('pivots.api.urls'))
]
