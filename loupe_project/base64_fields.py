import base64
from tastypie.fields import FileField
from django.core.files.uploadedfile import SimpleUploadedFile

class Base64FileField(FileField):
    """
    A django-tastypie field for handling file-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.

    Usage:

        class MyResource(ModelResource):
            file_field = Base64FileField("file_field")

            class Meta:
                queryset = ModelWithFileField.objects.all()

    In the case of multipart for submission, it would also pass the filename.
    By using a raw post data stream, we have to pass the filename within our
    file_field structure:

        file_field = {"name": "myfile.png", "file": "longbas64encodedstring"}
    """

    def hydrate(self, obj):
        value = super(Base64FileField, self).hydrate(obj)
        if value:
            value = SimpleUploadedFile(value["name"], base64.b64decode(value["file"]))
            return value
        return None
