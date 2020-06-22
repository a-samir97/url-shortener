# to short the URL
from hashlib import md5

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from graphql import GraphQLError

class ShortURL(models.Model):

    full_url = models.URLField(unique=True)
    short_url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.short_url = md5(self.full_url.encode()).hexdigest()[:10]
        
        validate = URLValidator()

        try:
            validate(self.full_url)
        except ValidationError:
            raise GraphQLError("invalid url")
        
        return super().save(*args, **kwargs)
