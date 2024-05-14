import uuid
from django.db import models
from datetime import datetime

class User(models.Model):
    ROLES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('IO', 'Island Organizer'),
        ('CW', 'Content Writer'),
    ]

    # id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    phone_numbers = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    domicile = models.CharField(max_length=255)
    verified = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLES, default="User")

class Organizer(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    phone_numbers = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    domicile = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=255)
    island_name = models.CharField(max_length=70, choices=[('Sumatera', 'Sumatera'), ('Sulawesi', 'Sulawesi'), ('Kalimantan', 'Kalimantan'), ('Jawa', 'Jawa'), ('Papua', 'Papua'), ('Timor', 'Timor')])
    trip_date = models.DateField()
    duration = models.CharField(max_length=225)
    open_registration = models.DateField()
    close_registration = models.DateField()
    objective = models.TextField()
    preparation = models.TextField()
    capacity = models.IntegerField()
    skills = models.CharField(max_length=255)
    vroles = models.CharField(max_length=255)
    captain = models.CharField(max_length=225)
    users = models.ManyToManyField(User, through='UserTrip')
    trip_pic = models.ImageField(default='default_pic.jpeg')


class UserTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phoneNum = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    experience = models.TextField(blank=True, null=True)
    application_status = models.CharField(max_length=50, choices=[('applied', 'Applied'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')])
    class Meta:
        unique_together = ['user', 'trip']

class TripQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()

class TripAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(TripQuestion, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.TextField()
    

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    htrip = models.IntegerField()
    hconfirmed = models.IntegerField()
    hrejected = models.IntegerField()
    hcancelled = models.IntegerField()


class VolunteerMetrics(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, swappable=True)
    application_rate = models.FloatField()
    completion_rate = models.FloatField()
    feedback_score = models.IntegerField()

class Merchandise(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    story = models.TextField()
    highlighted = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

class Fund(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    link = models.URLField()
    purpose = models.TextField()
    highlighted = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

LANGUANGE_CHOICES = (
    ("en", "en"),
    ("id", "id")
)

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    highlighted = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    languange = models.CharField(max_length=5, choices=LANGUANGE_CHOICES, default="en")

class UserMetrics(models.Model):
    user = models.ForeignKey(Blog, on_delete=models.CASCADE)
    views = models.IntegerField()
    unique = models.IntegerField()
    cvisits = models.IntegerField()
    bounce = models.FloatField()
    mduration = models.TimeField()
    gtu_rate = models.FloatField()
    utv_rate = models.FloatField()

class FundLandingPage(models.Model):
    bg_landing = models.ImageField()
    title = models.CharField(max_length=255)
    content = models.TextField()

class FundWriting(models.Model):
    content_pic = models.ImageField()
    title = models.CharField(max_length=255)
    content = models.TextField()

class MerchandiseSection(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()  # diisi markdown

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()

class HomePageSection(models.Model):
    SECTION_TYPES = (
        ('hero', 'Hero'),
        ('impact', 'Impact Numbers'),
        ('trusted_by', 'Trusted By'),
        ('why_join', 'Why Join Card'),
    )
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default='hero')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homepage_images/', null=True, blank=True)
    video = models.FileField(upload_to='homepage_videos/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    
class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    vision = models.TextField()
    mision = models.TextField()
    visited = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

