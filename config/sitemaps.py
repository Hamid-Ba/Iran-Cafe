from django.contrib.sitemaps import Sitemap
from django.utils.http import urlencode

from config import settings
from province import models as province_models
from cafe import models as cafe_models

SITE = getattr(settings, 'SITE')

def build_sitemap():
    sitemap = {
        'static' : StaticSitemap,
        'cafes' : CafesSitemap,
        'cafe' : CafeSitemap
    }
    return sitemap

class BaseSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8
    limit = 10000
    protocol = SITE.get('front').get('protocol')

def get_cafe_province_url(slug):
    return f'cafe:cafes_by_province/{slug}/'

class StaticSitemap(BaseSitemap):
    def items(self) :
        return ['','aboutUs','contactUs']

    def location(self, obj):
        return f'/{obj}'
        

class CafesSitemap(BaseSitemap):
    changefreq = 'yearly'

    def items(self):
        data = []
        for province in province_models.Province.objects.all():
            data.append(
                urlencode(
                            {
                                'province': province.slug,
                                'id' : province.id
                            }
                )
            )
        return data

    def location(self, addr):
        return f'/cafes?{addr}'

class CafeSitemap(BaseSitemap):
    changefreq = 'monthly'

    def items(self):
        data = []
        for cafe in cafe_models.Cafe.objects.all():
            data.append(
                urlencode(
                            {
                                '' : cafe.id
                            }
                )
            )
        return data

    def location(self, addr):
        addr = addr.replace('=' , '')
        return f'/cafes/{addr}'            