from django.contrib import admin
from django.urls import path
# from sonicjyotish.views import index_view
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
]

#urlpatterns = [
 #   path('admin/', admin.site.urls),
    #  path('', index_view, name='index'),  # főoldal
#]
