from django.db import models
from django.conf import settings

class Comment(models.Model):
    """Commnet Model"""
    date = models.DateField(auto_now_add=True)
    is_cafe = models.BooleanField(default=False)
    text = models.CharField(max_length=500, blank=False, null=False)
    cafe_id = models.PositiveBigIntegerField(null=False, blank=False)
    item_id = models.PositiveBigIntegerField(null=False, blank=False)

    response = models.OneToOneField('self',on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user')

    def __str__(self) :
        return f'{self.user} - item : {self.item_id}'