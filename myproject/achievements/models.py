from django.db import models
from django.contrib.auth.models import User


class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100)
    # Add other researcher-specific fields
    # Add additional fields here
    # Example:
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# To ensure a Researcher profile is created whenever a User is created,
from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Researcher.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.researcher.save()


class Achievement(models.Model):
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Add more fields specific to the type of achievement


# You can define more models for specific types of achievements, like Articles, Patents, etc.


class Article(models.Model):
    # Relation to Researcher model
    # Assuming a many-to-many relationship, as an article can have multiple authors and a researcher can author multiple articles
    researchers = models.ManyToManyField(Researcher, related_name="articles")

    # Basic article information
    title = models.CharField(max_length=255)
    doi = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )  # DOI is unique if present

    # Journal information
    journal_name = models.CharField(max_length=255, blank=True)
    impact_factor = models.FloatField(
        null=True, blank=True
    )  # Can be blank or null if not known

    # Co-author information
    number_of_co_authors = models.PositiveIntegerField(default=0)
    number_of_co_authors_from_organization = models.PositiveIntegerField(default=0)

    # Additional fields like link to resources, file uploads etc.
    link_to_resource = models.URLField(blank=True, null=True)
    file_upload = models.FileField(upload_to="articles/", blank=True, null=True)

    # Meta information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
