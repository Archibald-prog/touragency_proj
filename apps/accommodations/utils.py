import random
from pytils.translit import slugify
from apps.accommodations import models


def get_random_id(top=True):
    """
    Returns a list of IDs of accommodations
    to be retrieved from the database
    """
    if top:
        initial_qs = models.Accommodation.objects.filter(is_top=True)
    else:
        initial_qs = models.Accommodation.objects.filter(is_new=True)
    random_list = random.sample(list(initial_qs), 8)
    random_id = [obj.id for obj in random_list]
    return random_id


def gen_slug(instance, slug):
    """Generates unique slugs for models"""
    model = instance.__class__
    unique_slug = slugify(slug)
    qs = model.objects.filter(slug=unique_slug).order_by('-id')
    while qs.exists():
        unique_slug = f'{unique_slug}-{qs.first().id}'
    return unique_slug
