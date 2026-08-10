from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:lang>/comics/', views.comic_list, name='comic_list'),
    path('<str:lang>/', views.index, name='index'),
    path('<str:lang>/comics/<int:number>/', views.page, name='page'),
    path('<str:lang>/about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)