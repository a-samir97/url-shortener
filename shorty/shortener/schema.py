from django.db.models import Q

import graphene
from graphene_django import DjangoObjectType

from .models import ShortURL



class URLType(DjangoObjectType):
    class Meta:
        model = ShortURL


class Query(graphene.ObjectType):
    urls = graphene.List(URLType, url=graphene.String())

    def resolve_urls(self, info, url=None, **kwargs):
        queryset = ShortURL.objects.all()

        # filtering full urls 
        if url:
            queryset = ShortURL.objects.filter(Q(full_url__icontains=url))
        
        return queryset

class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    class Arguments:
        full_url = graphene.String()
    
    def mutate(self, info, full_url):
        url = ShortURL(full_url=full_url)
        url.save()

        return CreateURL(url=url)

class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()