from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User
from django_extensions.db.models import TitleSlugDescriptionModel

from imagekit.models import ImageModel

class Project(TitleSlugDescriptionModel):
    """
    Stores the projects that corkboards belong to.
    Only administrators should be able to set these up
    """

    user = models.ForeignKey(User)
    members = models.ManyToManyField(User, related_name="ProjectMember")
    created_on = models.DateTimeField(_('Created On'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField(_('Updated On'), editable=False, null=True, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __unicode__(self):
        return '%s' % (self.title)

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super(Project, self).save()

class Corkboard(TitleSlugDescriptionModel):
    """
    Stores the grouping of images to be reviewed by the project team
    Example.  For a home page mockup this group would contain all mockups
    for only the home page to reduce confusion when reviewing designs.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    created_on = models.DateTimeField(_('Created On'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField(_('Updated On'), editable=False, null=True, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __unicode__(self):
        return '%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('corkboard_detail', (), {
            'slug': self.slug,
        })

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super(Corkboard, self).save()

class Image(ImageModel):
    title = models.CharField(max_length=200)
    corkboard = models.ForeignKey(Corkboard)
    original_image = models.ImageField(upload_to='loupe')
    user = models.ForeignKey(User)
    num_views = models.PositiveIntegerField(_('Number of Views'), editable=False, default=0)
    created_on = models.DateTimeField(_('Created On'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField(_('Updated On'), editable=False, null=True, blank=True)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'loupe.specs'
        cache_dir = 'loupe'
        image_field = 'original_image'
        save_count_as = 'num_views'

    def __unicode__(self):
        return '%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('image_detail', (), {
            'id': self.id,
        })

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super(Image, self).save()

class Note(models.Model):
    """
    Stores image notes for the jquery hover blocks that are placed
    over the images
    """
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    note = models.TextField(_('Note'))
    x1 = models.PositiveIntegerField(_('x1'), default=0)
    y1 = models.PositiveIntegerField(_('y1'), default=0)
    height = models.PositiveIntegerField(_('Height'), default=20)
    width = models.PositiveIntegerField(_('Width'), default=20)
    created_on = models.DateTimeField(_('Created On'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField(_('Updated On'), editable=False, null=True, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __unicode__(self):
        return '%s' % (self.note)

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super(Note, self).save()
