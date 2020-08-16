from django.utils import timezone
# import json
# from apps.products.models import ListItem


def return_date_time():
    return timezone.now()


def upload_location_blog(instance, filename):
    return "blog/%s" % (filename,)


def upload_location_media(instance, filename):
    return "sources/%s" % (filename,)


def remove_script_tags(string):
    import re
    clean = re.compile('<script.*?script>')
    return re.sub(clean, '', string)


def pagination_wrapper(request, query):
    from django.core.paginator import Paginator
    from django.conf import settings

    order = '-date_published'

    if 'order' in request.GET and request.GET['order'] == 'oldest':
        order = 'date_published'

    posts_list = query.order_by(order)
    paginator = Paginator(posts_list, settings.DEFAULT_PAGINATION_SIZE) # Show 9 posts per page.
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    return queryset
