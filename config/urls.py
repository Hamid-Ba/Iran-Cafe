"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from django.contrib import admin
from django.urls import (path,include)
from django.contrib.sitemaps.views import sitemap

from config.sitemaps import CafesSitemap ,CafeSitemap, StaticSitemap , build_sitemap
from siteinfo.views import RobotsView

sitemaps = {
    'static' : StaticSitemap,
    'cafes' : CafesSitemap,
    'cafe' : CafeSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(),name = "api-schema"),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name ='api-schema'),
        name = 'api-docs',
    ),
    path('sitemap.xml',sitemap,{'sitemaps' : build_sitemap()}),
    path('robots.txt', RobotsView.as_view(), name='robots.txt'),
    path('api/account/',include('account.urls')),
    path('api/cafe/',include('cafe.urls')),
    path('api/blog/',include('blog.urls')),
    path('api/comment/',include('comment.urls')),
    path('api/siteinfo/',include('siteinfo.urls')),
    path('api/plan/',include('plan.urls')),
    path('api/payment/',include('payment.urls')),
    path('api/queries/',include('queries.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)