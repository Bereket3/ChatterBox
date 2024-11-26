from django.db import models


class MessageContent(models.Model):
    text_content = models.TextField()
    file_name = models.CharField(max_length=400, blank=True, null=True)
    file_content = models.FileField(upload_to="upload_content/", blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file_name.__str__()


class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255, default=None, null=True)
    message = models.ForeignKey(MessageContent, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room)
