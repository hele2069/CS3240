from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from chat.models import Room

class Courses(models.Model):
    subject = models.CharField("Subject", max_length=255)
    number = models.CharField("Number", max_length=4)
    instructor = models.CharField("Instructor", max_length=255)
    # users = models.OneToOneField(, on_delete=models.CASCADE)

    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.subject + self.number


# one-to-one database relationship (between user and user profile)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    courses = models.ManyToManyField(Courses)
    toggled_courses = models.ManyToManyField(Courses, related_name='toggled_courses', blank=True)

    # courses_id = models.IntegerField(default=00000)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Schedule(models.Model):
    # user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, default=None)
    study_buddies = models.ManyToManyField(Profile, default=None)
    common_course = models.CharField("Course(s)", max_length=100)
    time = models.DateTimeField()
    location = models.CharField("Location", max_length=5000)

# class Match(models.Model):
#     users = models.ManyToManyField(User)
#     course_match = models.OneToOneField(Courses, on_delete=models.CASCADE)
#     room = models.OneToOneField(Room, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.room.slug
