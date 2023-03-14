from django.db import models

# Create your models here.


class StoreCategory(models.Model):
    title = models.CharField(max_length=255)
    sortitem = models.IntegerField(default=0)
    sub_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"
