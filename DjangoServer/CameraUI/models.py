import base64

from django.db import models


class Person(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    face_descriptor = models.BinaryField()
    photo = models.BinaryField()

    def get_image(self):
        return base64.b64encode(self.photo).decode('utf-8')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class Sighting(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    sighting_time = models.DateTimeField(auto_now_add=True)
    camera_photo = models.BinaryField()

    def get_image(self):
        return base64.b64encode(self.camera_photo).decode('utf-8')

    def __str__(self):
        return f"{self.person} {self.sighting_time}"
