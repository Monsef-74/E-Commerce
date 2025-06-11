from django.db import models

class TryOnResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    result_image = models.ImageField(upload_to='tryon_results/')
    result_image_2 = models.ImageField(upload_to='tryon_results/', null=True, blank=True)  
