from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, RichTextFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


class JobPostingPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        RichTextFieldPanel('body'),
    ]


class JobPostingListPage(Page):
    subpage_types = ['JobPostingPage',
                     ]

    jobs_per_page = models.IntegerField(default=10)

    @property
    def subpages(self):
        subpages = JobPostingPage.objects.live().order_by('-first_published_at')
        return subpages

    def get_context(self, request):
        jobs = self.subpages

        page = request.GET.get('page')
        paginator = Paginator(jobs, self.jobs_per_page)
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        context = super(JobPostingListPage, self).get_context(request)
        context['jobs'] = jobs
        return context

    content_panels = Page.content_panels + [
        FieldPanel('jobs_per_page'),
    ]
