from django.urls import path
from app.views import index, home

urlpatterns = [
    path('api/', index, name='handler'),
    path('home/', home, name='home'),
]
