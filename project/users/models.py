from django.db import models
from django.contrib.auth.models import AbstractUser,User, Group, Permission
from PIL import Image
# Create your models here.



class User(AbstractUser):
    is_association= models.BooleanField(default=False)
    is_donor = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')
   
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='dashboard_donor')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    objects = models.Manager() #### why??????
    
    def __str__(self):
        return "Donor Name : " + self.user.first_name
    
class Association(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='dashboard_association')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    stat_juridique=models.CharField(max_length=50, null=True, blank=True)
    objects = models.Manager() #### why??????
    
    def __str__(self):
        return "Association Name : " + self.user.first_name
  


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='dashboard_admin')
    image = models.ImageField(upload_to='admin/profile', default='Default/user.png')
    objects = models.Manager() #### why??????
    
    def __str__(self):
        return "Admin Name : " + self.user.first_name
 








class Profile(models.Model):

    # chaque user a un profile unique + si on supprime user , le profile sera supprimer également
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    
    avatar=models.ImageField(
        default='avatar.jpg',
        upload_to = 'profile_avatar'
    )
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.avatar.path) # Open an image file
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)