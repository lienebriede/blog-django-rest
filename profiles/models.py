from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../ftpfkey8ogd3f06e0vle'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

    # ensures that a profile is created every time a user is created
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance)
    # listen for the post_save signal coming from User model and call the connect function
    post_save.connect(create_profile, sender=User)