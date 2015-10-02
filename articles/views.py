from django.http import JsonResponse
from wagtail.wagtailcore.models import Page


def social_share_count(request, page_id):

    page = Page.objects.specific().get(id=page_id)

    page.update_cache()

    twitter_shares = page.twitter_count
    facebook_shares = page.facebook_count
    return JsonResponse({'twitter': twitter_shares,
                         'facebook': facebook_shares})
