from tastypie import fields
from loupe.models import Project, Corkboard, Image, Note
from django.contrib.auth.models import User
from django.db.models import Q
from base64_fields import Base64FileField
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpCreated
from tastypie.utils import dict_strip_unicode_keys
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

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get("CONTENT_TYPE", "application/json"))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized))
        self.is_valid(bundle, request)
        ## add user into obj_create, this is the only difference between std tastypie implementation
        updated_bundle = self.obj_create(bundle, request=request, user=request.user)
        return HttpCreated(location=self.get_resource_uri(updated_bundle))

    def get_object_list(self, request, *args, **kwargs):
        return Project.objects.filter(Q(members=request.user) | Q(user=request.user))

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

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get("CONTENT_TYPE", "application/json"))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized))
        self.is_valid(bundle, request)
        ## add user into obj_create, this is the only difference between std tastypie implementation
        updated_bundle = self.obj_create(bundle, request=request, user=request.user)
        return HttpCreated(location=self.get_resource_uri(updated_bundle))

    images = fields.ToManyField("loupe.api.ImageResource", "image_set", full=True)

    def get_object_list(self, request, *args, **kwargs):
        return Corkboard.objects.filter(Q(project__members=request.user) | Q(project__user=request.user))

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
        return Image.objects.filter(Q(corkboard__project__members=request.user) | Q(corkboard__project__members=request.user))

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get("CONTENT_TYPE", "application/json"))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized))
        self.is_valid(bundle, request)
        ## add user into obj_create, this is the only difference between std tastypie implementation
        updated_bundle = self.obj_create(bundle, request=request, user=request.user)
        return HttpCreated(location=self.get_resource_uri(updated_bundle))

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
        return Note.objects.filter(Q(image__corkboard__project__members=request.user) | Q(image__corkboard__project__members=request.user))

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get("CONTENT_TYPE", "application/json"))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized))
        self.is_valid(bundle, request)
        ## add user into obj_create, this is the only difference between std tastypie implementation
        updated_bundle = self.obj_create(bundle, request=request, user=request.user)
        return HttpCreated(location=self.get_resource_uri(updated_bundle))

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
