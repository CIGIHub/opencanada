from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from wagtail.wagtailadmin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class ContributorListPage(Page):
    subpage_types = ['ContributorPage']

    people_per_page = models.IntegerField(default=20)

    @property
    def contributors(self):
        contributors = ContributorPage.objects.live().descendant_of(self).order_by('last_name', 'first_name')
        return contributors

    def get_context(self, request):
        people = self.contributors

        page = request.GET.get('page')
        paginator = Paginator(people, self.people_per_page)
        try:
            people = paginator.page(page)
        except PageNotAnInteger:
            people = paginator.page(1)
        except EmptyPage:
            people = paginator.page(paginator.num_pages)

        context = super(ContributorListPage, self).get_context(request)
        context['people'] = people
        return context

    content_panels = Page.content_panels + [
        FieldPanel('people_per_page')
    ]


@python_2_unicode_compatible
class ContributorPage(Page):
    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    nickname = models.CharField(max_length=1024, blank=True, default="")

    email = models.EmailField(blank=True, default="")
    twitter_handle = models.CharField(max_length=16, blank=True, default="")

    short_bio = models.TextField(blank=True, default="")
    long_bio = models.TextField(blank=True, default="")

    headshot = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('first_name', partial_match=True),
        index.SearchField('last_name', partial_match=True),
        index.SearchField('twitter_handle', partial_match=True),
        index.SearchField('short_bio', partial_match=True),
        index.SearchField('long_bio', partial_match=True),
    )

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.title = "{} {}".format(self.first_name, self.last_name)
        elif self.first_name:
            self.title = self.first_name
        elif self.last_name:
            self.title = self.last_name
        elif self.nickname:
            self.title = self.nickname
        else:
            if not self.title:
                self.title = ""
        self.slug = slugify(self.title)
        if self.twitter_handle and not self.twitter_handle.startswith("@"):
            self.twitter_handle = "@{}".format(self.twitter_handle)
        super(ContributorPage, self).save(*args, **kwargs)

        if not self.slug:
            self.title = str(self.id)
            self.slug = slugify(self.title)
            self.save()

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def last_comma_first_name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    @property
    def display_twitter_handle(self):
        if self.twitter_handle:
            return self.twitter_handle[1:]
        return self.twitter_handle

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)


ContributorPage.content_panels = [
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('email'),
    FieldPanel('twitter_handle'),
    RichTextFieldPanel('short_bio'),
    RichTextFieldPanel('long_bio'),
    ImageChooserPanel('headshot'),
]
