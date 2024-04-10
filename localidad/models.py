from django.db import models

# Create your models here.

#____________________________________________________________________________________________________________
#MODELO REGION 

class Region(models.Model):
    region = models.CharField(max_length=100, verbose_name='Region')
    
    def __str__(self):
        return self.region
        
#____________________________________________________________________________________________________________

#MODELO COMUNA QUE HEREDA LA REGION DEL MODELO "REGION"
class Comuna(models.Model):
    comuna = models.CharField(max_length=100, verbose_name='Comuna')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.comuna}'
        
