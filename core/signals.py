from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Client


# def client_profile(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.get(name='clients')
#         instance.groups.add(group)

#         Client.objects.create(
#             user=instance,
#             nickname=instance.username
#         )
#         print('Client profile created!')


# post_save.connect(client_profile, sender=User)
