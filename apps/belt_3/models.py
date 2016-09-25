from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, name, alias, email, password, passconf, dob):
        errors = []
        if len(name) < 2:
            errors.append('Name must be at least 2 characters')
        if not NAME_REGEX.match(name):
            errors.append('Name may only contain letters')
        if len(alias) < 2:
            errors.append('Alias must be at least 2 characters')
        if not NAME_REGEX.match(alias):
            errors.append('Alias may only contain letters')
        if not EMAIL_REGEX.match(email):
            errors.append('invalid email')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        if passconf != password:
            errors.append('Password confirmation must match password')
        if len(dob) < 8:
            errors.append('invalid date of birth length')
        if len(dob) >= 8:
            s = dob
            f = "%Y-%m-%d"
            date = datetime.datetime.strptime(s, f)
            if date > datetime.datetime.now():
                errors.append("You arent born yet...")
        if len(errors) > 0:
            return (errors, None)
        else:
            check_email = User.objects.filter(email = email.lower())
            if len(check_email) > 0:
                return(['Already in the system'], None)
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name = name,alias = alias,email = email,password = pw_hash, dob = dob)
            return (None, 'user')

    def login(self, email, password):
        user = User.objects.filter(email = email)
        if len(user) > 0:
            user = user[0]
            if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
                return (None, user)
        return (['Wrong login'], None)

class QuoteManager(models.Manager):
    def add_quote(self, person, quote):
        errors = []
        if len(person) < 4:
            errors.append("person quoted must be 4 or more charaters")
        if len(person) > 30:
            errors.append("person quoted must be less than 31 charaters")
        if len(quote) < 11:
            errors.append("quote must be 11 or more charaters")
        if len(person) > 300:
            errors.append("quote must be less than 301 charaters")
        if len(errors) > 0:
            return (errors, None)
        else:
            return (None, 'quotes')


class User(models.Model):
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    dob = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
    objects = models.Manager()

class Quote(models.Model):
    creator = models.ForeignKey(User)#creator of quote
    person = models.CharField(max_length=30)
    quote = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quoteManager = QuoteManager()
    objects = models.Manager()

class Favorite(models.Model):
    user_like = models.ForeignKey(User, related_name="user_liked")
    quote_like = models.ForeignKey(Quote, related_name="quote_liked", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
