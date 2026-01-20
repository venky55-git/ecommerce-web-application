from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def avg_rating(reviews):
    return reviews.aggregate(Avg('rating'))['rating__avg'] or 0