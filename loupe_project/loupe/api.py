from tastypie import fields
from loupe.models import Project, Corkboard, Image, Note
from django.contrib.auth.models import User
from base64_fields import Base64FileField
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
#from django.contrib.comments.models import Comment

from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        excludes = ["password", "is_active", "is_staff", "is_superuser"]
        allowed_methods = ["get"]
        filtering = {
            'username': ALL,
            'email': ALL
        }

class ProjectResource(ModelResource):

    corkboards = fields.ToManyField("loupe.api.CorkboardResource", "corkboard_set", full=True)

    def get_object_list(self, request, *args, **kwargs):
        return Project.objects.filter(members=request.user)

    class Meta:
        queryset = Project.objects.all()
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ["get", "post"]
        ordering = ['created_on', 'updated_on']
        filtering = {
            'members': ALL_WITH_RELATIONS,
            'title': ALL,
            'description': ALL,
        }

class CorkboardResource(ModelResource):

    images = fields.ToManyField("loupe.api.ImageResource", "image_set", full=True)

    def get_object_list(self, request, *args, **kwargs):
        return Corkboard.objects.filter(project__members=request.user)

    class Meta:
        queryset = Corkboard.objects.all()
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ["get", "post"]
        ordering = ['created_on', 'updated_on']
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'title': ALL,
            'description': ALL,
        }

class ImageResource(ModelResource):
    original_image = Base64FileField("original_image", null=True)
    notes = fields.ToManyField("loupe.api.NoteResource", "note_set", full=True)

    def get_object_list(self, request, *args, **kwargs):
        return Image.objects.filter(corkboard__project__members=request.user)

    class Meta:
        queryset = Image.objects.all()
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ["get", "post"]
        ordering = ['created_on', 'updated_on']
        filtering = {
            'corkboard': ALL_WITH_RELATIONS,
            'title': ALL,
            'description': ALL,
        }

class NoteResource(ModelResource):

    def get_object_list(self, request, *args, **kwargs):
        return Note.objects.filter(image__corkboard__project__members=request.user)

    class Meta:
        queryset = Note.objects.all()
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ["get", "post"]
        ordering = ['created_on', 'updated_on']
        filtering = {
            'image': ALL_WITH_RELATIONS,
            'title': ALL,
            'description': ALL,
        }
