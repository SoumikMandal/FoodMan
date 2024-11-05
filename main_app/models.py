from django.db import models
from mongoengine import Document, StringField

class User(Document):
    username = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)

    employee_id = StringField(default='')
    address = StringField(default='')
    contact = StringField(default='')

    meta = {
        'collection': 'User Authentication'
    }

class Enterprises(Document):
    enterprise_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)

    meta = {
        'db_alias': 'new_database',
        'collection': 'Enterprise Authentication'
    }

class partners(models.Model):
    image = models.ImageField(upload_to='partners/')

    def __str__(self):
        return f"Partner {self.id}"

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    company = models.ForeignKey(Company, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/')

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    

