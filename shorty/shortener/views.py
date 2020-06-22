from django.shortcuts import get_object_or_404, redirect

from .models import ShortURL


def index(request, short_url):
    url = get_object_or_404(ShortURL, short_url=short_url)
    url.clicked()

    return redirect(url.full_url)