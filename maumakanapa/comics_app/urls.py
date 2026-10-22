from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from comics_app.sitemaps import comicSitemap, staticSitemap
from . import views

sitemaps = {
    'static': staticSitemap,
    'webcomics': comicSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:lang>/comics/', views.comic_list, name='comic_list'),
    path('<str:lang>/', views.index, name='index'),
    path('<str:lang>/comics/<int:number>/comments/', views.create_episode_comment, name='comment_create'),
    path('<str:lang>/comics/<int:number>/comments/<int:comment_id>/edit/', views.edit_episode_comment, name='comment_edit'),
    path('<str:lang>/comics/<int:number>/comments/<int:comment_id>/delete/', views.delete_episode_comment, name='comment_delete'),
    path('<str:lang>/comics/<int:number>/comments/<int:comment_id>/like/', views.like_episode_comment, name='comment_like'),
    path('<str:lang>/comics/<int:number>/comments/<int:comment_id>/report/', views.report_episode_comment, name='comment_report'),
    path('<str:lang>/comics/<int:number>/', views.page, name='page'),
    path('<str:lang>/about/', views.about, name='about'),
    path('<str:lang>/rar/', views.revindex, name='revindex'),
    path('<str:lang>/tsrf/', views.tsrfindex, name='tsrfindex'),
    path('<str:lang>/tbtl/', views.tbtlindex, name='tbtlindex'),
    path('<str:lang>/mc/', views.mcindex, name='mcindex'),
    path('<str:lang>/xenobot/', views.xenobot, name='xenobot'),
    path('<str:lang>/ai/', views.ai, name='ai'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)