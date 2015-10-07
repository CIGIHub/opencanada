from __future__ import absolute_import, division, unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                ObjectList, RichTextFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from themes.models import ThemeablePage


class ContributorListPage(ThemeablePage):
    subpage_types = ['ContributorPage']

    def get_rows(self, contributors, number_of_columns=3, max_columns=4):
        rows = []
        number_of_items = len(contributors)
        number_of_rows = number_of_items // number_of_columns
        row_remainder = number_of_items % number_of_columns

        if row_remainder > number_of_rows:
            number_of_rows += 1
        elif row_remainder <= number_of_rows and row_remainder != 0:
            if number_of_columns < max_columns:
                number_of_columns += 1
            else:
                number_of_rows += 1

        for row_index in range(0, number_of_rows):
            row = contributors[(row_index * number_of_columns):(row_index * number_of_columns) + number_of_columns]
            rows.append(row)
        return rows

    @property
    def recent_contributors(self):
        endtime = timezone.now()
        starttime = endtime - datetime.timedelta(days=365)
        contributors = ContributorPage.objects.live().filter(featured=False,
                                                             article_links__article__isnull=False,
                                                             article_links__isnull=False,
                                                             article_links__article__first_published_at__range=[starttime, endtime]
                                                             ).order_by('last_name', 'first_name').distinct()
        return self.get_rows(contributors, number_of_columns=4)

    @property
    def nonfeatured_contributors(self):
        contributors = ContributorPage.objects.live().filter(featured=False).order_by('last_name', 'first_name')
        return self.get_rows(contributors)

    @property
    def featured_contributors(self):
        contributors = ContributorPage.objects.live().filter(featured=True).order_by('last_name', 'first_name')
        return self.get_rows(contributors)

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class ContributorPage(ThemeablePage):
    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    nickname = models.CharField(max_length=1024, blank=True, default="")

    email = models.EmailField(blank=True, default="")
    twitter_handle = models.CharField(max_length=16, blank=True, default="")

    short_bio = RichTextField(blank=True, default="")
    long_bio = RichTextField(blank=True, default="")

    headshot = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    featured = models.BooleanField(default=False)

    search_fields = Page.search_fields + (
        index.SearchField('first_name', partial_match=True),
        index.SearchField('last_name', partial_match=True),
        index.SearchField('twitter_handle', partial_match=True),
        index.SearchField('short_bio', partial_match=True),
        index.SearchField('long_bio', partial_match=True),
    )

    def search_result_text(self):
        if self.short_bio:
            self.search_result_text = self.short_bio
        else:
            self.search_result_text = self.long_bio[0:240]
        return self.search_result_text

    def save(self, *args, **kwargs):
        if self.twitter_handle and not self.twitter_handle.startswith("@"):
            self.twitter_handle = "@{}".format(self.twitter_handle)
        super(ContributorPage, self).save(*args, **kwargs)

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

    content_panels = Page.content_panels + [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('twitter_handle'),
        RichTextFieldPanel('short_bio'),
        RichTextFieldPanel('long_bio'),
        ImageChooserPanel('headshot'),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel('featured'),
            ],
            heading="Featuring Settings"
        )
    ]

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
