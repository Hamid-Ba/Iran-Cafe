"""
Province Module Models
"""
from django.db import models
from django.shortcuts import reverse

class Province(models.Model):
    """Province Model"""
    name = models.CharField(max_length=50,blank=False,null=False)
    slug = models.SlugField(max_length=125,blank=False,null=False)

    def __str__(self) :
        return self.name
    
    def get_absolute_url(self):
        return reverse('cafe:cafes_by_province',kwargs={'province_slug': self.slug})
    
        
class City(models.Model):
    """City Model"""
    name = models.CharField(max_length=85,blank=False,null=False)
    slug = models.SlugField(max_length=225,blank=False,null=False)
    province = models.ForeignKey(Province, null=False, blank=False,on_delete=models.CASCADE)

    def __str__(self) :
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'