from __future__ import unicode_literals

from django.db import models
from django.db.utils import OperationalError

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.models import Page, Orderable, Collection
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        FieldRowPanel,
        StreamFieldPanel,
        MultiFieldPanel,
        PageChooserPanel
        )
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from .blocks import BaseStreamBlock
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField


@register_snippet
class People(ClusterableModel):
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('first_name', classname="col6"),
        FieldPanel('last_name', classname="col6"),
        FieldPanel('job_title'),
        ImageChooserPanel('image')
    ]

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    api_fields = [
        'first_name',
        'last_name',
        'job_title',
        'image'
    ]


class AboutLocationRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `LocationPage` within the `locations`
    app and the About page below allowing us to add locations to the about
    section.
    """
    page = ParentalKey(
        'AboutPage', related_name='location_about_relationship'
    )
    locations = models.ForeignKey(
        'locations.LocationPage', related_name='about_location_relationship'
    )
    panels = [
        PageChooserPanel('locations')
    ]


class AboutPage(Page):
    """
    The About Page
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Location image'
    )

    body = StreamField(
        BaseStreamBlock(), verbose_name="About page detail", blank=True
        )
    # We've defined the StreamBlock() within blocks.py that we've imported on
    # line 12. Defining it in a different file gives us consistency across the
    # site, though StreamFields _can_ be created on a per model basis if you
    # have a use case for it

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        InlinePanel(
           'location_about_relationship',
           label='Locations',
           min_num=None
           ),
    ]

    def locations(self):
        locations = [
             n.people for n in self.location_about_relationship.all()
        ]

        return locations

    # parent_page_types = [
    #    'home.HomePage'
    # ]

    # Defining what content type can sit under the parent
    # The empty array means that no children can be placed under the
    # LocationPage page model
    subpage_types = []

    # For ForeignKeys that we want to access via the API we need to explictly
    # access a specific field from the related content. I've added unnecessary
    # verbosity here because we could use the `locations(self)` method above to
    # give us the objects in a list within the for loop.
    # This isn't terribly useful since I'm only returning the title but hopefully
    # enough to be extendable/ understandable
    def locations_object(obj):
        locations_set = obj.location_about_relationship.all()
        locations = [
            n.locations for n in locations_set
        ]
        for location in locations:
            return location.title

    api_fields = [
        'title',
        'image',
        'body',
        'locations_object'
    ]


class GalleryPage(Page):
    """
    This is a page to list all the locations on the site
    """
    choices = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Location listing image'
    )

    introduction = models.TextField(
        help_text='Text to describe the index page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('choices'),
        ImageChooserPanel('image'),
        FieldPanel('introduction')
    ]

    # parent_page_types = [
    #     'home.HomePage'
    # ]

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    subpage_types = [
    ]

    # api_fields = ['introduction']


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
