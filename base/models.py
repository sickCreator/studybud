from django.db import models
# built in django user model
from django.contrib.auth.models import User
# Create your models here.
# a room is child of a topic


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # we are allowing topic to be null when host is deleted in the data base as SET_NULL is there.
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # created many to many relation
    # as User is already used we use a realaed name like participants
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    # every save
    updated = models.DateTimeField(auto_now=True)
    # only ssnapshot of initial save
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    # one to may relationship as message can only have one user.
    # django already has a builtin user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # to specify one to many relationship a room attribute will be used
    # SET_NULL to keep msg in db even after del rom
    # CASCADE to delete all the data for the room.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # every save
    updated = models.DateTimeField(auto_now=True)
    # only snapshot of initial save
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        # if the message is too long we only need the first 50 characters
        return self.body[0:50]
