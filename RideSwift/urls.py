from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from driver import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('signin/', login, name="login"),


    path('administrator/', include('Administrator.urls')),
    path('driver/', include('driver.urls')),
    path('user/', include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
